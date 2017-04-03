import signal

from gpiozero import Button

from . import notifier, settings

button = Button(settings.GPIO_INPUT_PIN)
button.when_pressed = notifier.notify_recipients

def run():
    print('Running')
    try:
        signal.pause()
    except KeyboardInterrupt:
        print('Done')
        return
