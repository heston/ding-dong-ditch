import datetime
import functools
import logging
import signal

import blinker

from . import action, notifier, user_settings

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


def get_strike_setting_path(unit_id):
    return '/{}/strike'.format(unit_id)


def handle_gate_strike_unit_1(sender, value=None):
    if not value:
        return
    logger.info('Trigger activated for gate strike in unit 1')
    action.UNIT_1.strike.release()
    user_settings.set_data(get_strike_setting_path(action.UNIT_1.id), 0)


def handle_gate_strike_unit_2(sender, value=None):
    if not value:
        return
    logger.info('Trigger activated for gate strike in unit 2')
    action.UNIT_2.strike.release()
    user_settings.set_data(get_strike_setting_path(action.UNIT_2.id), 0)


action.UNIT_1.buzzer.when_pressed = trigger_unit_1
action.UNIT_2.buzzer.when_pressed = trigger_unit_2
blinker.signal(
    get_strike_setting_path(action.UNIT_1.id)
).connect(handle_gate_strike_unit_1)
blinker.signal(
    get_strike_setting_path(action.UNIT_2.id)
).connect(handle_gate_strike_unit_2)


def run():
    logger.info('Up and running')
    try:
        signal.pause()
    except KeyboardInterrupt:
        logger.info('Shutting down')
