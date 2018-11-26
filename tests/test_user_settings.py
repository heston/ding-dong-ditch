import pytest

from dingdongditch import user_settings, firebase_user_settings_adapter


@pytest.fixture
def adapter(mocker):
    get_adapter = mocker.patch('dingdongditch.user_settings.get_adapter')
    return get_adapter.return_value


@pytest.fixture
def get_data(mocker):
    return mocker.patch('dingdongditch.user_settings.get_data')


@pytest.fixture
def set_data(mocker):
    return mocker.patch('dingdongditch.user_settings.set_data')


def test_get_adapter__unknown(settings):
    settings(USER_SETTINGS_ADAPTER='foo_adapter')

    with pytest.raises(ValueError):
        user_settings.get_adapter()


def test_get_adapter__valid(settings):
    settings(USER_SETTINGS_ADAPTER='firebase')
    adapter = user_settings.get_adapter()
    assert adapter is firebase_user_settings_adapter


def test_get_data__error(adapter, mocker):
    adapter.get_settings.side_effect = TypeError
    logger_mock = mocker.patch('dingdongditch.user_settings.logger')

    with pytest.raises(TypeError):
        user_settings.get_data()

    assert logger_mock.exception.called


def test_get_data__valid(adapter):
    adapter.get_settings.return_value.is_stale = False
    user_settings.get_data()

    assert adapter.get_settings.called


def test_set_data__error(adapter, mocker):
    adapter.set_data.side_effect = TypeError
    logger_mock = mocker.patch('dingdongditch.user_settings.logger')

    with pytest.raises(TypeError):
        user_settings.set_data('foo', 'bar')

    assert logger_mock.exception.called


def test_set_data__default_root(adapter):
    user_settings.set_data('foo', 'bar')

    adapter.set_data.assert_called_with('foo', 'bar', None)


def test_set_data__custom_root(adapter):
    user_settings.set_data('foo', 'bar', 'baz')

    adapter.set_data.assert_called_with('foo', 'bar', 'baz')


def test_signal(adapter):
    user_settings.signal('foo', bar='baz')

    adapter.signal.assert_called_with('foo', bar='baz')


def test_init_system_data__single_unit(mocker, settings, set_data):
    settings(UNIT_1=mocker.Mock(id='1111'))

    user_settings.init_system_data()

    set_data.assert_called_with('units', { '1111': 1}, '/systemSettings')


def test_init_system_data__dual_units(mocker, settings, set_data):
    settings(
        UNIT_1=mocker.Mock(id='1111'),
        UNIT_2=mocker.Mock(id='2222')
    )

    user_settings.init_system_data()

    set_data.assert_called_with(
        'units',
        {
            '1111': 1,
            '2222': 1,
        },
        '/systemSettings'
    )


def test_init_user_data__single_unit(mocker, settings, set_data, get_data):
    settings(UNIT_1=mocker.Mock(id='1111'))

    user_settings.init_user_data()

    set_data.assert_called_with('1111/strike', 0)
    assert get_data.called


def test_init_user_data__dual_units(mocker, settings, set_data, get_data):
    settings(
        UNIT_1=mocker.Mock(id='1111'),
        UNIT_2=mocker.Mock(id='2222')
    )

    user_settings.init_user_data()

    set_data.assert_has_calls([
        mocker.call('1111/strike', 0),
        mocker.call('2222/strike', 0)
    ])
    assert get_data.called


def test_init_data(mocker):
    init_system_data = mocker.patch('dingdongditch.user_settings.init_system_data')
    init_user_data = mocker.patch('dingdongditch.user_settings.init_user_data')

    user_settings.init_data()

    assert init_system_data.called
    assert init_user_data.called


def test_reset(mocker, adapter, get_data):
    init_user_data = mocker.patch('dingdongditch.user_settings.init_user_data')

    user_settings.reset()

    assert adapter.reset.called
    assert init_user_data.called


def test_get_unit_by_id__missing_data(get_data):
    get_data.return_value = None

    result = user_settings.get_unit_by_id(1234)

    assert result is None


def test_get_unit_by_id__missing_unit(get_data):
    get_data.return_value = {
        '5678': {}
    }

    result = user_settings.get_unit_by_id(1234)

    assert result is None


def test_get_unit_by_id__valid_unit__int_id(get_data):
    get_data.return_value = {
        '1234': {}
    }

    result = user_settings.get_unit_by_id(1234)

    assert isinstance(result, user_settings.Unit)


    def test_get_unit_by_id__valid_unit__string_id(get_data):
        get_data.return_value = {
            '1234': {}
        }

        result = user_settings.get_unit_by_id('1234')

        assert isinstance(result, user_settings.Unit)


def test_get_unit_by_id__valid_unit__defaults(get_data):
    get_data.return_value = {
        '1234': {}
    }

    result = user_settings.get_unit_by_id(1234)

    assert result.should_ring_bell == 1
    assert isinstance(result.recipients, dict)
    assert len(result.recipients) == 0


def test_get_unit_by_id__valid_unit__should_ring_bell(get_data):
    get_data.return_value = {
        '1234': {
            'chime': 1
        }
    }

    result = user_settings.get_unit_by_id(1234)

    assert result.should_ring_bell


def test_get_unit_by_id__valid_unit__not_should_ring_bell(get_data):
    get_data.return_value = {
        '1234': {
            'chime': 0
        }
    }

    result = user_settings.get_unit_by_id(1234)

    assert not result.should_ring_bell


def test_get_unit_by_id__valid_unit__empty_recipients(get_data):
    get_data.return_value = {
        '1234': {
            'recipients': None
        }
    }

    result = user_settings.get_unit_by_id(1234)

    assert isinstance(result.recipients, dict)


def test_get_unit_by_id__valid_unit__recipients(get_data):
    get_data.return_value = {
        '1234': {
            'recipients': {
                '+14155551001': 1,
                'asdf1234=': 2,
            }
        }
    }

    result = user_settings.get_unit_by_id(1234)

    assert result.recipients == {
        '+14155551001': 1,
        'asdf1234=': 2,
    }
