import datetime
import functools
import logging
import signal

from . import action, notifier, system_settings, user_settings

WINDOW = datetime.timedelta(seconds=system_settings.BUZZER_INTERVAL)
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
    logger.debug('Trigger activated for unit 1')
    notifier.notify_recipients(action.UNIT_1.id)


@throttle(WINDOW)
def trigger_unit_2():
    logger.debug('Trigger activated for unit 2')
    notifier.notify_recipients(action.UNIT_2.id)


def get_strike_setting_path(unit_id):
    return '/{}/strike'.format(unit_id)


def handle_gate_strike_unit_1(sender, value=None):
    if not value:
        return
    logger.info('Gate strike activated for unit 1')
    action.UNIT_1.strike.release(system_settings.STRIKE_RELEASE_DURATION)
    user_settings.set_data(get_strike_setting_path(action.UNIT_1.id), 0)


def handle_gate_strike_unit_2(sender, value=None):
    if not value:
        return
    logger.info('Gate strike activated for unit 2')
    action.UNIT_2.strike.release(system_settings.STRIKE_RELEASE_DURATION)
    user_settings.set_data(get_strike_setting_path(action.UNIT_2.id), 0)


if action.UNIT_1:
    action.UNIT_1.buzzer.when_held = trigger_unit_1
    action.UNIT_1.buzzer.when_pressed = lambda: logger.debug('Trigger pressed for unit 1')
    user_settings.signal(
        get_strike_setting_path(action.UNIT_1.id)
    ).connect(handle_gate_strike_unit_1)


if action.UNIT_2:
    action.UNIT_2.buzzer.when_held = trigger_unit_2
    action.UNIT_2.buzzer.when_pressed = lambda: logger.debug('Trigger pressed for unit 2')
    user_settings.signal(
        get_strike_setting_path(action.UNIT_2.id)
    ).connect(handle_gate_strike_unit_2)


def run():
    logger.info('Up and running')
    try:
        signal.pause()
    except KeyboardInterrupt:
        logger.info('Shutting down')
