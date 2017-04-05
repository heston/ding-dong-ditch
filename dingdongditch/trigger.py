import datetime
import functools

import gevent
from gpiozero import Button

from . import notifier, settings

WINDOW = datetime.timedelta(seconds=15)


def throttle(window):
    def wrapper(func):
        state = {
            'last': None
        }

        @functools.wraps(func)
        def inner():
            now = datetime.datetime.now()
            if state['last'] is None or now - state['last'] > window:
                state['last'] = now
                func()
        return inner
    return wrapper


@throttle(WINDOW)
def trigger():
    print('Triggered!')
    notifier.notify_recipients()


button = Button(settings.GPIO_INPUT_PIN)
button.when_pressed = trigger


def run():
    print('Running')
    print('Watching GPIO pin: ', settings.GPIO_INPUT_PIN)
    try:
        while True:
            gevent.sleep(1)
    except KeyboardInterrupt:
        print('Done\n')
        return
