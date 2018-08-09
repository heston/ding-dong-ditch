import datetime

import blinker
import pytest

from dingdongditch import firebase_user_settings_adapter


@pytest.fixture(autouse=True)
def live_data(mocker):
    return mocker.patch('dingdongditch.firebase_user_settings_adapter.live_data')



def test_get_settings(live_data):
    firebase_user_settings_adapter.get_settings()

    assert live_data.get_data.called


class Test_set_data:
    def test_default_root(self, live_data):
        data = object()
        firebase_user_settings_adapter.set_data('foo', data)

        live_data.set_data.assert_called_with('/settings/foo', data)

    def test_custom_root(self, live_data):
        data = object()
        firebase_user_settings_adapter.set_data('foo', data, 'bar')

        live_data.set_data.assert_called_with('bar/foo', data)

    def test_missing_root(self, live_data):
        data = object()
        firebase_user_settings_adapter.set_data('foo', data, None)

        live_data.set_data.assert_called_with('/settings/foo', data)


def test_hangup(live_data):
    firebase_user_settings_adapter.hangup()

    assert live_data.hangup.called


def test_reset(live_data):
    firebase_user_settings_adapter.reset()

    assert live_data.reset.called
