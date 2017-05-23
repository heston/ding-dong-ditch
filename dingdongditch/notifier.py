import logging
import urllib.parse

from twilio.rest import Client

from . import action, system_settings, user_settings


logger = logging.getLogger(__name__)

client = Client(system_settings.TWILIO_SID, system_settings.TWILIO_TOKEN)

def get_twiml_response(unit_id):
    endpoint = 'http://twimlets.com/echo'
    action_url = '{}?pin={}'.format(
        system_settings.FIREBASE_CLOUD_FUNCTION_UNLOCK_URL,
        unit_id
    )
    twiml = (
        '<Response>'
            '<Gather method="GET" numDigits="1" action="{url}">'
                '<Say loop="5">'
                    'This is your doorbell calling. Someone is at the door. '
                    'Press any key to unlock the gate. '
                '</Say>'
            '</Gather>'
        '</Response>'
    ).format(url=action_url)

    querystring = urllib.parse.urlencode({'Twiml': twiml})
    return '{url}?{qs}'.format(url=endpoint, qs=querystring)

def notify(unit_id, number):
    try:
        call = client.calls.create(
            to=number,
            from_=system_settings.FROM_NUMBER,
            url=get_twiml_response(unit_id)
        )
        call.fetch()
    except Exception as e:
        logger.exception('Failed to notify recipient: %s. Error: %s', number, e)
    else:
        logger.info('Notified recipient: %s. Sid: %s', number, call.sid)
        return call.sid


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
        logger.info('Ringing bell in unit: %s', unit_id)
        action_unit = action.get_unit_by_id(unit_id)
        action_unit.bell.ring()

    for recipient in usr_unit.recipients:
        logger.info('Notifying unit "%s" recipient: %s', unit_id, recipient)
        notify(unit_id, recipient)
