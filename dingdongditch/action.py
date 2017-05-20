from collections import namedtuple
from gpiozero import Button, DigitalOutputDevice

from . import system_settings as settings

Unit = namedtuple('Unit', 'id buzzer bell strike')


class Strike(DigitalOutputDevice):
    """A class to represent an electronic gate strike."""

    def release(duration=1):
        """Release the strike, thus opening the door/gate it is guarding.

        Arguments:
            duration: The duration that the strike should remain open.
        """
        super(Strike, self).blink(on_time=duration, off_time=1, n=1, background=True)


class Bell(DigitalOutputDevice):
    """A class to represent a doorbell chime."""

    def ring(ding_dong=.5):
        """Ring a doorbell chime with a friendly DING-DONG sound.

        Arguments:
            ding_dong: The duration of the gap between "ding" and "dong", in seconds.
        """
        super(Bell, self).blink(on_time=duration, off_time=1, n=1, background=True)


UNIT_1 = Unit(
    id=settings.UNIT_1.id,
    buzzer=Button(settings.UNIT_1.buzzer),
    bell=Bell(settings.UNIT_1.bell),
    strike=Strike(settings.UNIT_1.strike)
)

UNIT_2 = Unit(
    id=settings.UNIT_2.id,
    buzzer=Button(settings.UNIT_2.buzzer),
    bell=Bell(settings.UNIT_2.bell),
    strike=Strike(settings.UNIT_2.strike)
)


def get_unit_by_id(unit_id):
    """
    Return a Unit by its ID.
    """
    if unit_id == UNIT_1.id:
        return UNIT_1
    elif unit_id == UNIT_2.id:
        return UNIT_2
    return None
