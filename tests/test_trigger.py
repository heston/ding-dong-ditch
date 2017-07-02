from dingdongditch import system_settings, trigger


def test_trigger_unit_1(mocker):
    unit_1_mock = mocker.patch('dingdongditch.action.UNIT_1')
    unit_1_mock.id = 1
    notify_mock = mocker.patch('dingdongditch.notifier.notify_recipients')

    trigger.trigger_unit_1()

    notify_mock.assert_called_with(1)


def test_trigger_unit_2(mocker):
    unit_2_mock = mocker.patch('dingdongditch.action.UNIT_2')
    unit_2_mock.id = 2
    notify_mock = mocker.patch('dingdongditch.notifier.notify_recipients')

    trigger.trigger_unit_2()

    notify_mock.assert_called_with(2)
