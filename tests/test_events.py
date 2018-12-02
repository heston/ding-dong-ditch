import time

import pytest

from dingdongditch import events


@pytest.fixture
def now(mocker):
    now = time.time()
    time_mock = mocker.patch('dingdongditch.events.time')
    time_mock.time.return_value = now
    return now


@pytest.fixture
def event_id(mocker):
    fake_event_id = 'a-b-c-d'
    event_id_mock = mocker.patch('dingdongditch.events.get_event_id')
    event_id_mock.return_value = fake_event_id
    return fake_event_id


def test_get_event_id():
    result = events.get_event_id()

    assert type(result) is str
    assert len(result) == 36


def test_get_event_path():
    unit_id = 1234
    event_id = 'a-b-c-d'
    result = events.get_event_path(unit_id, event_id)

    assert result == '1234/a-b-c-d'


def test_record_event__default_event_name(event_id, now, mocker):
    user_settings_mock = mocker.patch('dingdongditch.events.user_settings')
    unit_id = 1234

    result = events.record_event(unit_id)

    user_settings_mock.set_data.assert_called_with(
        '1234/a-b-c-d',
        {
            'name': 'doorbell',
            'occurredAt': now,
        },
        root='events'
    )
    assert result == event_id


def test_record_event__custom_event_name(event_id, now, mocker):
    user_settings_mock = mocker.patch('dingdongditch.events.user_settings')
    unit_id = 1234

    events.record_event(unit_id, 'my_event')

    user_settings_mock.set_data.assert_called_with(
        '1234/a-b-c-d',
        {
            'name': 'my_event',
            'occurredAt': now,
        },
        root='events'
    )
