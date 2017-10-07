from dingdongditch import notifier, system_settings, user_settings


def test__notify__success(mocker):
    client_mock = mocker.patch('dingdongditch.notifier.twilio_client')
    log_mock = mocker.patch('dingdongditch.notifier.logger')

    result = notifier.notify('1234', '+14155551001', 1)

    client_mock.calls.create.assert_called_with(
        to='+14155551001',
        from_=system_settings.FROM_NUMBER,
        url=mocker.ANY,
        if_machine='Hangup'
    )
    assert result is client_mock.calls.create.return_value.sid
    log_mock.info.assert_any_call(
        'Notifying unit "%s" recipient: %s', '1234', '+14155551001'
    )


def test__notify__failure(mocker):
    client_mock = mocker.patch('dingdongditch.notifier.twilio_client')
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    client_mock.calls.create.side_effect = Exception

    result = notifier.notify('1234', '+14155551001', 1)

    assert log_mock.exception.called
    assert result is False


def test__notify_recipients__unknown_unit_id(mocker):
    log_mock = mocker.patch('dingdongditch.notifier.logger')

    notifier.notify_recipients('1234')

    log_mock.warning.assert_called_with('Unknown unit id: %s', '1234')


def test__notify_recipients__unconfigured_unit(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )

    notifier.notify_recipients('1234')

    log_mock.warning.assert_called_with('Unit found but not yet configured: %s', '1234')


def test__notify_recipients__should_not_ring_bell(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )
    get_unit_by_id_mock = mocker.patch('dingdongditch.user_settings.get_unit_by_id')
    get_unit_by_id_mock.return_value = user_settings.Unit(
        should_ring_bell=False, recipients={}
    )
    notify_mock = mocker.patch('dingdongditch.notifier.notify')
    ring_mock = mocker.patch('dingdongditch.notifier.ring')

    notifier.notify_recipients('1234')

    assert not log_mock.warning.called
    assert not ring_mock.called


def test__notify_recipients__should_ring_bell(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )
    get_unit_by_id_mock = mocker.patch('dingdongditch.user_settings.get_unit_by_id')
    get_unit_by_id_mock.return_value = user_settings.Unit(
        should_ring_bell=True, recipients={}
    )
    ring_mock = mocker.patch('dingdongditch.notifier.ring')

    notifier.notify_recipients('1234')

    assert not log_mock.warning.called
    ring_mock.assert_called_with('1234')


def test__notify_recipients__should_call_recipients(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )
    get_unit_by_id_mock = mocker.patch('dingdongditch.user_settings.get_unit_by_id')
    get_unit_by_id_mock.return_value = user_settings.Unit(
        should_ring_bell=False, recipients={'+14155551001': 1}
    )
    notify_mock = mocker.patch('dingdongditch.notifier.notify')

    notifier.notify_recipients('1234')

    assert not log_mock.warning.called
    notify_mock.assert_called_with('1234', '+14155551001', 1)


def test__notify_recipients__no_network__no_fallback(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        RING_FALLBACK=False,
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )
    get_unit_by_id_mock = mocker.patch('dingdongditch.user_settings.get_unit_by_id')
    get_unit_by_id_mock.return_value = user_settings.Unit(
        should_ring_bell=False, recipients={'+14155551001': 1}
    )
    notify_mock = mocker.patch('dingdongditch.notifier.notify')
    notify_mock.return_value = False
    ring_mock = mocker.patch('dingdongditch.notifier.ring')

    notifier.notify_recipients('1234')

    log_mock.error.assert_called_with(
        'All notifications failed!'
    )
    assert not ring_mock.called


def test__notify_recipients__no_network__with_fallback(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        RING_FALLBACK=True,
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )
    get_unit_by_id_mock = mocker.patch('dingdongditch.user_settings.get_unit_by_id')
    get_unit_by_id_mock.return_value = user_settings.Unit(
        should_ring_bell=False, recipients={'+14155551001': 1}
    )
    notify_mock = mocker.patch('dingdongditch.notifier.notify')
    notify_mock.return_value = False
    ring_mock = mocker.patch('dingdongditch.notifier.ring')

    notifier.notify_recipients('1234')

    log_mock.error.assert_called_with(
        'All notifications failed!'
    )
    assert ring_mock.called
