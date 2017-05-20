from dingdongditch import system_settings, trigger

def test_trigger_unit_1(mocker):
    notify_mock = mocker.patch('dingdongditch.notifier.notify_recipients')
    trigger.trigger_unit_1()

    notify_mock.assert_called_with(system_settings.UNIT_1_ID)


def test_trigger_unit_2(mocker):
    notify_mock = mocker.patch('dingdongditch.notifier.notify_recipients')
    trigger.trigger_unit_2()

    notify_mock.assert_called_with(system_settings.UNIT_2_ID)
