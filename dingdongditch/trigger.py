import datetime
import functools
import logging

import gevent
from gpiozero import Button

from . import notifier, settings

WINDOW = datetime.timedelta(seconds=15)
logger = logging.getLogger(__name__)


def throttle(window):
    def wrapper(func):
        state = {
            'last': None
        }

        logger.debug('function %s throttled at %s', func, window)

        @functools.wraps(func)
        def inner():
            now = datetime.datetime.now()
            elapsed = now - state['last']
            if state['last'] is None or elapsed > window:
                state['last'] = now
                logger.debug('throttle executing: %s', func)
                func()
            else:
                logger.debug('throttle skipping: %s. Elapsed window: %s', func, elapsed)
        return inner
    return wrapper


@throttle(WINDOW)
def trigger():
    logger.info('Trigger activated')
    notifier.notify_recipients()


button = Button(settings.GPIO_INPUT_PIN)
button.when_pressed = trigger


def run():
    logger.info('Up and running')
    logger.info('Watching GPIO pin: %s', settings.GPIO_INPUT_PIN)
    try:
        while True:
            gevent.sleep(1)
    except KeyboardInterrupt:
        logger.info('Shutting down')
        return
