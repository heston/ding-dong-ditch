import datetime
import functools
import logging
import signal

from . import action, notifier

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
def trigger_unit_1():
    logger.debug('Trigger activated in unit 1')
    notifier.notify_recipients(action.UNIT_1.id)


@throttle(WINDOW)
def trigger_unit_2():
    logger.debug('Trigger activated in unit 2')
    notifier.notify_recipients(action.UNIT_2.id)


action.UNIT_1.buzzer.when_pressed = trigger_unit_1
action.UNIT_2.buzzer.when_pressed = trigger_unit_2


def run():
    logger.info('Up and running')
    try:
        signal.wait()
    except KeyboardInterrupt:
        logger.info('Shutting down')
