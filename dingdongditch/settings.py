import logging
import os

from .utils import Env

LOG_PATH = os.path.dirname(__file__)
LOG_FILE = 'app.log'

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
    filename=os.path.join(LOG_PATH, LOG_FILE),
    level=logging.DEBUG
)

# Twilio REST API credentials
TWILIO_SID = Env.string('TWILIO_SID')
TWILIO_TOKEN = Env.string('TWILIO_SECRET_TOKEN')

# "From" phone number associated with the Twilio account
FROM_NUMBER = Env.string('TWILIO_FROM_NUMBER')

# Comma-separated list of recipient phone numbers
RECIPIENTS = [r.strip() for r in Env.string('TWILIO_RECIPIENTS').split(',')]

# The GPIO input pin number that will pull up when the doorbell is rung
GPIO_INPUT_PIN = 21
