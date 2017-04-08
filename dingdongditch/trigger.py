import datetime
import functools
import logging
import signal

from gpiozero import Button

from . import notifier, settings

WINDOW = datetime.timedelta(seconds=15)
logger = logging.getLogger(__name__)


def trigger():
    logger.info('Trigger activated')
    notifier.notify_recipients()


button = Button(
    settings.GPIO_INPUT_PIN,
    bounce_time=float(WINDOW.seconds)
)
button.when_pressed = trigger


def run():
    logger.info('Up and running')
    logger.info('Watching GPIO pin: %s', settings.GPIO_INPUT_PIN)
    try:
        signal.wait()
    except KeyboardInterrupt:
        logger.info('Shutting down')
