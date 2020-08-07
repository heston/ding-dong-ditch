from concurrent import futures
from datetime import datetime
from enum import IntEnum
from functools import lru_cache
import logging
from operator import itemgetter

from pyfcm import FCMNotification
from pyfcm.errors import FCMError
from twilio.rest import Client

from . import action, system_settings, user_settings

logger = logging.getLogger(__name__)

PUSH_MSG_TITLE = 'Ding Dong'
PUSH_MSG_BODY = 'Your doorbell is ringing!'
SMS_TEMPLATE = 'Ding dong! Your doorbell rang {}'
SMS_TIME_FORMAT = '%b %d, %I:%M:%S %p'  # Mar 31, 9:45:03 AM
PHONE_POSTFIX_DELIMITER = '::'

executor = futures.ThreadPoolExecutor(
    max_workers=system_settings.NOTIFIER_THREADPOOL_SIZE
)


@lru_cache()
def get_push_service(api_key=None):
    return FCMNotification(api_key=api_key or system_settings.FIREBASE_FCM_KEY)


@lru_cache()
def get_twilio_client(sid=None, token=None):
    return Client(
        sid or system_settings.TWILIO_SID,
        token or system_settings.TWILIO_TOKEN
    )


class RecipientType(IntEnum):
    PHONE = 1
    SMS = 2
    PUSH = 3


def parse_phone_number(phone_string):
    if phone_string:
        return phone_string.split(PHONE_POSTFIX_DELIMITER)[0]


def get_twiml_url(unit_id):
    return '{}?pin={}'.format(
        system_settings.FIREBASE_CLOUD_FUNCTION_NOTIFY_URL,
        unit_id
    )


def get_sms_body():
    now = datetime.now().strftime(SMS_TIME_FORMAT)
    return SMS_TEMPLATE.format(now)


def notify_with_future(unit_id, recipient, recipient_type, event_id=None):
    return executor.submit(notify, unit_id, recipient, recipient_type, event_id)


def notify(unit_id, recipient, recipient_type, event_id=None):
    logger.info('Notifying unit "%s" recipient: %s', unit_id, recipient)

    if recipient_type == RecipientType.PHONE:
        number = parse_phone_number(recipient)
        return notify_by_phone(unit_id, number)

    if recipient_type == RecipientType.PUSH:
        return notify_by_push(unit_id, recipient, event_id)

    if recipient_type == RecipientType.SMS:
        number = parse_phone_number(recipient)
        return notify_by_sms(unit_id, number)

    logger.error(
        'Unknown recipient type "%s" for "%s" in unit "%s"',
        recipient_type,
        recipient,
        unit_id
    )
    return False


def notify_by_phone(unit_id, number):
    logger.info('Notifying unit "%s" by phone "%s"', unit_id, number)
    try:
        call = get_twilio_client().calls.create(
            to=number,
            from_=system_settings.FROM_NUMBER,
            url=get_twiml_url(unit_id),
            if_machine='Hangup'  # Don't leave a message
        )
        call.fetch()
    except Exception as e:
        logger.exception('Failed to notify recipient: %s. Error: %s', number, e)
        return False
    else:
        logger.info('Notified recipient: %s. Sid: %s', number, call.sid)
        return call.sid


def notify_by_sms(unit_id, number):
    logger.info('Notifying unit "%s" by SMS "%s"', unit_id, number)
    try:
        msg = get_twilio_client().messages.create(
            to=number,
            from_=system_settings.FROM_NUMBER,
            body=get_sms_body())
        msg.fetch()
    except Exception as e:
        logger.exception('Failed to notify recipient: %s. Error: %s', number, e)
        return False
    else:
        logger.info('Notified recipient: %s. Sid: %s', number, msg.sid)
        return msg.sid


def notify_by_push(unit_id, token, event_id=None):
    logger.info('Notifying unit "%s" by push "%s"', unit_id, token)
    try:
        response = get_push_service().single_device_data_message(
            registration_id=token,
            time_to_live=0,  # "now or never"
            data_message={
                'title': PUSH_MSG_TITLE,
                'body': PUSH_MSG_BODY,
                'event_id': event_id,
            }
        )
        result = response['results'][0]
        if result.get('error'):
            raise FCMError(result['error'])
    except Exception as e:
        logger.exception('Failed to notify recipient: %s. Error: %s', token, e)
        return False
    else:
        message_id = result['message_id']
        logger.info('Notified recipient: %s. Message ID: %s', token, message_id)
        return message_id


def ring(unit_id):
    logger.info('Ringing bell in unit: %s', unit_id)
    action_unit = action.get_unit_by_id(unit_id)
    action_unit.bell.ring()


def _get_sorted_recipients(recipients):
    return sorted(recipients.items(), key=itemgetter(1), reverse=True)


def notify_recipients(unit_id, event_id=None):
    sys_unit = system_settings.get_unit_by_id(unit_id)
    if not sys_unit:
        logger.warning('Unknown unit id: %s', unit_id)
        return

    usr_unit = user_settings.get_unit_by_id(unit_id)
    if not usr_unit:
        logger.warning('Unit found but not yet configured: %s', unit_id)
        return

    if usr_unit.should_ring_bell:
        ring(unit_id)

    # notify everyone at once
    all_futures = [
        notify_with_future(unit_id, recipient, recipient_type, event_id) for
        (recipient, recipient_type) in
        _get_sorted_recipients(usr_unit.recipients)
    ]

    # Gather all results, as they complete.
    # True means the notification succeeded. False means it failed.
    failures = [not f.result() for f in futures.as_completed(all_futures)]

    # If all notifications failed, fallback to normal bell, if enabled
    if usr_unit.recipients and all(failures):
        logger.error('All notifications failed!')
        if system_settings.RING_FALLBACK:
            ring(unit_id)
