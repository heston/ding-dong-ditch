import time

import pytest

from dingdongditch import system_settings, trigger


@pytest.fixture
def now(mocker):
    now = time.time()
    time_mock = mocker.patch('dingdongditch.trigger.time')
    time_mock.time.return_value = now
    return now


@pytest.fixture
def event_id(mocker):
    fake_event_id = 'a-b-c-d'
    event_id_mock = mocker.patch('dingdongditch.events.get_event_id')
    event_id_mock.return_value = fake_event_id
    return fake_event_id


def test_trigger_unit_1(mocker, event_id):
    unit_1_mock = mocker.patch('dingdongditch.action.UNIT_1')
    unit_1_mock.id = 1
    notify_mock = mocker.patch('dingdongditch.notifier.notify_recipients')

    trigger.trigger_unit_1()

    notify_mock.assert_called_with(1, event_id)


def test_trigger_unit_2(mocker, event_id):
    unit_2_mock = mocker.patch('dingdongditch.action.UNIT_2')
    unit_2_mock.id = 2
    notify_mock = mocker.patch('dingdongditch.notifier.notify_recipients')

    trigger.trigger_unit_2()

    notify_mock.assert_called_with(2, event_id)


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
