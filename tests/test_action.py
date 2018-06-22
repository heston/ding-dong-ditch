from gpiozero import DigitalOutputDevice

from dingdongditch import action


class TestStrike:
    def test_new_instance(self):
        instance = action.Strike(1)
        assert instance

    def test_get__new_instance(self):
        instance = action.Strike.get(1)
        assert instance

    def test_get__existing_instance(self):
        instance1 = action.Strike.get(1)
        instance2 = action.Strike.get(1)
        assert instance1 is instance2

    def test_release__default(self, mocker):
        instance = action.Strike(1)
        blink_mock = mocker.patch.object(DigitalOutputDevice, 'blink', create=True)

        instance.release()

        blink_mock.assert_called_with(on_time=3, off_time=1, n=1, background=True)

    def test_release__zero(self, mocker):
        instance = action.Strike(1)
        blink_mock = mocker.patch.object(DigitalOutputDevice, 'blink', create=True)

        instance.release(0)

        blink_mock.assert_called_with(on_time=3, off_time=1, n=1, background=True)

    def test_release__none(self, mocker):
        instance = action.Strike(1)
        blink_mock = mocker.patch.object(DigitalOutputDevice, 'blink', create=True)

        instance.release(None)

        blink_mock.assert_called_with(on_time=3, off_time=1, n=1, background=True)

    def test_release__custom(self, mocker):
        instance = action.Strike(1)
        blink_mock = mocker.patch.object(DigitalOutputDevice, 'blink', create=True)

        instance.release(10)

        blink_mock.assert_called_with(on_time=10, off_time=1, n=1, background=True)
