import time

import pytest

from dingdongditch import system_settings, trigger


@pytest.fixture
def now(mocker):
    now = time.time()
    time_mock = mocker.patch('dingdongditch.time')
    time_mock.time.return_value = now
    return now


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


def test_get_last_updated_path():
    path = trigger.get_last_updated_path()

    assert path == '/systemSettings/lastSeenAt'


def test_handle_last_updated(mocker, now):
    mocker.patch('dingdongditch.trigger.get_last_updated_path').return_value = '/foo'
    set_data_mock = mocker.patch('dingdongditch.user_settings.set_data')

    trigger.handle_last_updated(object())

    set_data_mock.assert_called_with(
        '/foo',
        now,
        root='/'
    )
