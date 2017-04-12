from gpiozero import DigitalOutputDevice

from . import settings


class Strike(DigitalOutputDevice):
    """A class to represent an electronic gate strike."""

    def release(duration=1):
        """Release the strike, thus opening the door/gate it is guarding.

        Arguments:
            duration: The duration that the strike should remain open.
        """
        super(Strike, self).blink(on_time=duration, off_time=1, n=1, background=True)


front_gate = Strike(settings.GPIO_OUTPUT_PIN)
