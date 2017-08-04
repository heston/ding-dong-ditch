from collections import namedtuple
import logging
import os
import sys

from .utils import Env


##
## Logging
##

# Options are: file, stdout
LOG_METHOD = Env.string('DDD_LOG_METHOD', 'stdout')
LOG_LEVEL = Env.string('DDD_LOGGING_LEVEL', 'INFO')
LOG_PATH = Env.string('DDD_LOG_PATH', os.path.dirname(__file__))
LOG_FILE = Env.string('DDD_LOG_FILE', 'ding-dong-ditch.log')

basicConfig_args = dict(
    format='[%(asctime)s] %(levelname)s %(name)s: %(message)s',
    level=LOG_LEVEL
)

if LOG_METHOD == 'file':
    basicConfig_args['filename'] = os.path.join(LOG_PATH, LOG_FILE)
elif LOG_METHOD == 'stdout':
    basicConfig_args['stream'] = sys.stdout
else:
    raise ValueError('Unknown value for LOG_METHOD: {}'.format(LOG_METHOD))

logging.basicConfig(**basicConfig_args)

if LOG_LEVEL is not 'DEBUG':
    # Configure some sub-loggers to be quieter, unless the global level is DEBUG
    connectionpool_logger = logging.getLogger('requests.packages.urllib3.connectionpool')
    connectionpool_logger.setLevel(logging.WARNING)

    oauth_logger = logging.getLogger('oauth2client.client')
    oauth_logger.setLevel(logging.WARNING)


##
## Twilio
##

# Twilio REST API credentials
TWILIO_SID = Env.string('DDD_TWILIO_SID')
TWILIO_TOKEN = Env.string('DDD_TWILIO_SECRET_TOKEN')

# "From" phone number associated with the Twilio account
FROM_NUMBER = Env.string('DDD_FROM_NUMBER')


##
## Hardware Interface
##

# The throttle rate of the doorbell trigger, in seconds.
BUZZER_INTERVAL = Env.number('DDD_BUZZER_INTERVAL', 30)

# The time (in seconds) to wait after the buzzer is pushed to notify recipients.
BUZZER_HOLD = Env.number('DDD_BUZZER_HOLD', 0.3)

# Whether to always ring the bell, regardless of user setting, when the network is down
RING_FALLBACK = Env.boolean('DDD_RING_FALLBACK', True)


##
## Unit 1
##

# The ID of Unit 1. This will also be the dial-in PIN.
UNIT_1_ID = Env.string('DDD_UNIT_1_ID')

# The GPIO input pin number that will pull up when the doorbell is rung
GPIO_INPUT_PIN_BELL_1 = Env.number('DDD_GPIO_INPUT_PIN_BELL_1')

# The GPIO output pin that will trigger the traditional doorbell
GPIO_OUTPUT_PIN_BELL_1 = Env.number('DDD_GPIO_OUTPUT_PIN_BELL_1')

# The GPIO output pin that will trigger the gate opener/strike
GPIO_OUTPUT_PIN_STIKE_1 = Env.number('DDD_GPIO_OUTPUT_PIN_STRIKE_1')

##
## Unit 2
##

# The ID of Unit 2. This will also be the dial-in PIN.
UNIT_2_ID = Env.string('DDD_UNIT_2_ID')

# The GPIO input pin number that will pull up when the doorbell is rung
GPIO_INPUT_PIN_BELL_2 = Env.number('DDD_GPIO_INPUT_PIN_BELL_2')

# The GPIO output pin that will trigger the traditional doorbell
GPIO_OUTPUT_PIN_BELL_2 = Env.number('DDD_GPIO_OUTPUT_PIN_BELL_2')

# The GPIO output pin that will trigger the gate opener/strike
GPIO_OUTPUT_PIN_STIKE_2 = Env.number('DDD_GPIO_OUTPUT_PIN_STRIKE_2')


##
## Firebase
##

# The data source for user settings. Currently, only Firebase is supported.
USER_SETTINGS_ADAPTER = 'firebase'

# The name of the Firebase app, used to construct the REST URL.
FIREBASE_APP_NAME = Env.string('DDD_FIREBASE_APP_NAME', 'ding-dong-ditch')

# The URL to the Firebase Cloud Function that initiates the voice doorbell.
FIREBASE_CLOUD_FUNCTION_NOTIFY_URL = Env.string('DDD_FIREBASE_CLOUD_FUNCTION_NOTIFY_URL')

# Path to service account credentials file
FIREBASE_KEY_PATH = Env.string('DDD_FIREBASE_KEY_PATH', '/home/pi/.firebasekey')

# Firebase web API key
FIREBASE_API_KEY = Env.string('DDD_FIREBASE_API_KEY')


##
## Unit configuration
##

# Representation of a unit in the building
Unit = namedtuple('Unit', 'id buzzer bell strike')

# The first unit
UNIT_1 = Unit(
    id=UNIT_1_ID,
    buzzer=GPIO_INPUT_PIN_BELL_1,
    bell=GPIO_OUTPUT_PIN_BELL_1,
    strike=GPIO_OUTPUT_PIN_STIKE_1
)

# The second unit
UNIT_2 = Unit(
    id=UNIT_2_ID,
    buzzer=GPIO_INPUT_PIN_BELL_2,
    bell=GPIO_OUTPUT_PIN_BELL_2,
    strike=GPIO_OUTPUT_PIN_STIKE_2
)


def get_unit_by_id(unit_id):
    """
    Return a Unit by its ID.
    """
    # unit ID should always be a string
    unit_id = str(unit_id)
    if unit_id == UNIT_1.id:
        return UNIT_1
    elif unit_id == UNIT_2.id:
        return UNIT_2
    return None
