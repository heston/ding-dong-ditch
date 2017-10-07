from enum import Enum
import logging

from pyfcm import FCMNotification
from pyfcm.errors import FCMError
from twilio.rest import Client

from . import action, system_settings, user_settings

logger = logging.getLogger(__name__)

twilio_client = Client(system_settings.TWILIO_SID, system_settings.TWILIO_TOKEN)
push_service = FCMNotification(api_key=system_settings.FIREBASE_FCM_KEY)

PUSH_MSG_TITLE = 'Ding Dong'
PUSH_MSG_BODY = 'Your doorbell is rining!'


def RecipientType(Enum):
    PHONE = 1
    PUSH = 2


def get_twiml_url(unit_id):
    return '{}?pin={}'.format(
        system_settings.FIREBASE_CLOUD_FUNCTION_NOTIFY_URL,
        unit_id
    )


def notify(unit_id, number, recipient_type):
    logger.info('Notifying unit "%s" recipient: %s', unit_id, number)

    if recipient_type == RecipientType.PHONE.value:
        notify_by_phone(unit_id, number)

    if recipient_type == RecipientType.PUSH.value:
        notify_by_push(unit_id, number)

    else:
        logger.error(
            'Unknown recipient type "%s" for number "%s" in unit "%s"',
            recipient_type,
            number,
            unit_id
        )


def notify_by_phone(unit_id, number):
    try:
        logger.info('Notifying unit "%s" by phone "%s"', unit_id, number)
        call = twilio_client.calls.create(
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


def notify_by_push(unit_id, token):
    logger.info('Notifying unit "%s" by push "%s"', unit_id, token)
    try:
        response = push_service.notify_single_device(
            registration_id=token,
            message_title=PUSH_MSG_TITLE,
            message_body=PUSH_MSG_BODY
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


def notify_recipients(unit_id):
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

    # notify everyone and track failures
    # TODO: Run each request in a separate thread
    failures = [
        not notify(unit_id, recipient, recipient_type) for
        (recipient, recipient_type) in
        usr_unit.recipients.items()
    ]

    # If all notifications failed, fallback to normal bell, if enabled
    if usr_unit.recipients and all(failures):
        logger.error('All notifications failed!')
        if system_settings.RING_FALLBACK:
            ring(unit_id)
