import datetime
import functools
import logging
import signal

from gpiozero import Button

from . import notifier, settings

WINDOW = datetime.timedelta(seconds=15)
logger = logging.getLogger(__name__)


def throttle(window):
    def wrapper(func):
        state = {
            'last': None
        }

        logger.debug('%s throttled at %s', func, window)

        @functools.wraps(func)
        def inner():
            now = datetime.datetime.now()
            if state['last'] is None or now - state['last'] > window:
                state['last'] = now
                logger.debug('throttle executing: %s', func)
                func()
            else:
                logger.debug(
                    'throttle skipping %s. Elapsed window is %s',
                    func,
                    now - state['last']
                )
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
        signal.wait()
    except KeyboardInterrupt:
        logger.info('Shutting down')
