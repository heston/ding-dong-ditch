import logging
import urllib.parse

import gevent
from twilio.rest import TwilioRestClient

from . import settings


logger = logging.getLogger(__name__)

client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)
endpoint = 'http://twimlets.com/echo'

twiml = (
    '<Response>'
        '<Say loop="5">'
            'This is your doorbell calling. Someone is at the door.'
        '</Say>'
    '</Response>'
)

querystring = urllib.parse.urlencode({'Twiml': twiml})


def notify(number):
    logger.debug('Notifying recipient: %s', number)
    try:
        call = client.calls.create(
            to=number,
            from_=settings.FROM_NUMBER,
            url='{url}?{qs}'.format(url=endpoint, qs=querystring)
        )
    except Exception as e:
        logger.exception('Failed to notify recipient: %s. Error: %s', number, e)
    else:
        logger.info('Notified recipient: %s. Sid: %s', number, call.sid)
        return call.sid


def notify_recipients():
    greenlets = []
    for recipient in settings.RECIPIENTS:
        greenlets.append(gevent.spawn(notify, recipient))
    gevent.wait(greenlets)
    return greenlets
