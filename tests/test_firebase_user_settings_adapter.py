import datetime

import blinker
import pytest

from dingdongditch import firebase_user_settings_adapter as user_settings


class Test_get_path_list:
    def test_no_path(self):
        data = user_settings.FirebaseData()
        result = user_settings._get_path_list('')
        assert result == []

    def test_root_path(self):
        data = user_settings.FirebaseData()
        result = user_settings._get_path_list('/')
        assert result == []

    def test_absolute_child_path(self):
        data = user_settings.FirebaseData()
        result = user_settings._get_path_list('/foo/bar')
        assert result == ['foo', 'bar']

    def test_relative_child_path(self):
        data = user_settings.FirebaseData()
        result = user_settings._get_path_list('foo/bar')
        assert result == ['foo', 'bar']


class TestFirebaseData_set:
    def test_set_root(self):
        data = user_settings.FirebaseData()
        data.set('/', {'foo': 1})
        assert data == {'foo': 1}

    def test_set_missing_child(self):
        data = user_settings.FirebaseData()
        data.set('/foo/bar', 1)
        assert data == {'foo': {'bar': 1}}

    def test_set_existing_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_missing_then_set_existing(self):
        data = user_settings.FirebaseData()
        data.set('/foo', {'bar': 1})
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_different_type(self):
        data = user_settings.FirebaseData({'foo': 1})
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_missing_then_set_different_type(self):
        data = user_settings.FirebaseData()
        data.set('/foo', 1)
        data.set('/foo/bar', 2)
        assert data == {'foo': {'bar': 2}}

    def test_set_different_type_then_set_missing(self):
        data = user_settings.FirebaseData({'foo': 1})
        data.set('/foo/bar', 2)
        data.set('/foo/bar/baz', {'qux': 1})
        assert data == {'foo': {'bar': {'baz': {'qux': 1}}}}

    def test_unset_root(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.set('/', None)
        assert data == {}

    def test_unset_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.set('/foo/bar', None)
        assert data == {'foo': {}}

    def test_unset_missing_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.set('/foo/bar/baz', None)
        assert data == {'foo': {'bar': {}}}


class TestFirebaseData_get:
    def test_get_root(self):
        data = user_settings.FirebaseData()
        result = data.get('/')
        assert result == {}

    def test_get_missing_key(self):
        data = user_settings.FirebaseData()
        result = data.get('/foo/bar')
        assert result == None

    def test_get_different_type_key(self):
        data = user_settings.FirebaseData({'foo': 1})
        result = data.get('/foo/bar')
        assert result == None

    def test_existing_key(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        result = data.get('/foo/bar')
        assert result == 1


class TestFirebaseData_merge:
    def test_merge_root(self):
        data = user_settings.FirebaseData()
        data.merge('/', {'foo/bar': 1})
        assert data == {'foo': {'bar': 1}}

    def test_merge_missing(self):
        data = user_settings.FirebaseData()
        data.merge('/foo', {'bar': 1})
        assert data == {'foo': {'bar': 1}}

    def test_merge_simple_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.merge('/foo', {'baz': 1})
        assert data == {'foo': {'bar': 1, 'baz': 1}}

    def test_merge_nested_child(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.merge('/', {'foo/baz': 1})
        assert data == {'foo': {'bar': 1, 'baz': 1}}

    def test_merge_nested_child_overwrite(self):
        data = user_settings.FirebaseData({'foo': {'bar': 1}})
        data.merge('/', {'foo/bar/baz': 1})
        assert data == {'foo': {'bar': {'baz': 1}}}


class TestFirebaseData_pubsub:
    def test_receive_event(self, mocker):
        data = user_settings.FirebaseData()
        listen_mock = mocker.MagicMock()

        def listener(*args, **kwargs):
            listen_mock(*args, **kwargs)

        blinker.signal('/foo/bar').connect(listener)

        data.set('/foo/bar', 2)
        listen_mock.assert_called_with(data, value=2)


class TestFirebaseData_staleness:
    def test_last_updated_at__set_on_init(self):
        data = user_settings.FirebaseData()

        assert isinstance(data.last_updated_at, datetime.datetime)


    def test_last_updated_at__somehow_missing(self):
        data = user_settings.FirebaseData()
        data.last_updated_at = None

        assert data.is_stale

    def test_is_stale__is_not_stale(self):
        data = user_settings.FirebaseData()

        assert not data.is_stale

    def test_is_stale__is_stale(self):
        data = user_settings.FirebaseData()
        data.last_updated_at = datetime.datetime.utcnow() - datetime.timedelta(hours=2)

        assert data.is_stale

    def test_is_stale__is_not_stale_after_update(self):
        data = user_settings.FirebaseData()
        data.last_updated_at = datetime.datetime.utcnow() - datetime.timedelta(hours=2)

        data.set('foo', 'bar')
        assert not data.is_stale


class Test_get_settings:
    def test_cold_cache(self, mocker):
        listen_mock = mocker.patch('dingdongditch.firebase_user_settings_adapter.listen')

        result = user_settings.get_settings()

        assert 'user_settings' in user_settings._cache
        assert listen_mock.called
        assert isinstance(result, user_settings.FirebaseData)

    def test_warm_cache(self, mocker):
        mock_settings = mocker.MagicMock()
        user_settings._cache['user_settings'] = mock_settings

        result = user_settings.get_settings()

        assert result is mock_settings


def test_put_settings_handler(mocker):
    mock_settings = mocker.MagicMock()
    user_settings._cache['user_settings'] = mock_settings

    path = '/foo/bar'
    data = 1
    user_settings._put_settings_handler(path, data)

    mock_settings.set.assert_called_with(path, data)


def test_patch_settings_handler(mocker):
    mock_settings = mocker.MagicMock()
    user_settings._cache['user_settings'] = mock_settings

    path = '/'
    data = {'foo/bar': 1}
    user_settings._patch_settings_handler(path, data)

    mock_settings.merge.assert_called_with(path, data)


def test_stream_handler__put(mocker):
    put_handler_mock = mocker.patch(
        'dingdongditch.firebase_user_settings_adapter._put_settings_handler'
    )

    message = {
        'data': {
            '1': {
                'strike': 0,
                'chime': 0,
                'recipients': {
                    '+14155551000': 1
                }
            }
        },
        'event': 'put',
        'path': '/'
    }
    user_settings._stream_handler(message)

    put_handler_mock.assert_called_with(message['path'], message['data'])


def test_stream_handler__patch(mocker):
    patch_handler_mock = mocker.patch(
        'dingdongditch.firebase_user_settings_adapter._patch_settings_handler'
    )

    message = {
        'data': {
            '1/strike': 0
        },
        'event': 'patch',
        'path': '/'
    }
    user_settings._stream_handler(message)

    patch_handler_mock.assert_called_with(message['path'], message['data'])


@pytst.mark.skip(reason='Disabled until thread blocking is fixed')
def test_hangup(mocker):
    streams = {
        'user_settings': mocker.Mock(),
        'user_settings2': mocker.Mock(),
    }
    mocker.patch('dingdongditch.firebase_user_settings_adapter._streams', streams)

    user_settings.hangup()

    assert streams['user_settings'].close.called
    assert streams['user_settings2'].close.called


def test_reset(mocker):
    hangup = mocker.patch('dingdongditch.firebase_user_settings_adapter.hangup')
    _cache = mocker.patch('dingdongditch.firebase_user_settings_adapter._cache')

    user_settings.reset()

    assert hangup.called
    assert _cache.clear.called
