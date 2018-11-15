from dingdongditch import notifier, system_settings, user_settings


def test__notify_by_phone__success(mocker):
    client_mock = mocker.patch('dingdongditch.notifier.get_twilio_client').return_value
    log_mock = mocker.patch('dingdongditch.notifier.logger')

    result = notifier.notify_by_phone('1234', '+14155551001')

    client_mock.calls.create.assert_called_with(
        to='+14155551001',
        from_=system_settings.FROM_NUMBER,
        url=mocker.ANY,
        if_machine='Hangup'
    )
    assert result is client_mock.calls.create.return_value.sid
    log_mock.info.assert_any_call(
        'Notifying unit "%s" by phone "%s"', '1234', '+14155551001'
    )


def test__notify_by_phone__failure(mocker):
    client_mock = mocker.patch('dingdongditch.notifier.get_twilio_client').return_value
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    client_mock.calls.create.side_effect = Exception

    result = notifier.notify_by_phone('1234', '+14155551001')

    assert log_mock.exception.called
    assert result is False


def test__notify_by_push__success(mocker):
    service_mock = mocker.patch('dingdongditch.notifier.get_push_service').return_value
    log_mock = mocker.patch('dingdongditch.notifier.logger')

    result = notifier.notify_by_push('1234', 'asdf1234=')

    service_mock.notify_single_device.assert_called_with(
        registration_id='asdf1234=',
        data_message={
            'title': notifier.PUSH_MSG_TITLE,
            'body': notifier.PUSH_MSG_BODY,
        }
    )
    log_mock.info.assert_any_call(
        'Notifying unit "%s" by push "%s"', '1234', 'asdf1234='
    )


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


def test__notify_recipients__should_push_to_recipients(mocker, settings):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    settings(
        UNIT_1=system_settings.Unit(
            id='1234', buzzer=None, bell=None, strike=None
        )
    )
    get_unit_by_id_mock = mocker.patch('dingdongditch.user_settings.get_unit_by_id')
    get_unit_by_id_mock.return_value = user_settings.Unit(
        should_ring_bell=False, recipients={'asdf1234=': 2}
    )
    notify_mock = mocker.patch('dingdongditch.notifier.notify')

    notifier.notify_recipients('1234')

    assert not log_mock.warning.called
    notify_mock.assert_called_with('1234', 'asdf1234=', 2)


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


def test__notify__recipient_type__phone(mocker):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    notify_by_phone_mock = mocker.patch('dingdongditch.notifier.notify_by_phone')
    notify_by_push_mock = mocker.patch('dingdongditch.notifier.notify_by_push')

    notifier.notify('1234', '+14155551001', 1)

    notify_by_phone_mock.assert_called_with('1234', '+14155551001')
    assert not log_mock.error.called
    assert not notify_by_push_mock.called


def test__notify__recipient_type__push(mocker):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    notify_by_phone_mock = mocker.patch('dingdongditch.notifier.notify_by_phone')
    notify_by_push_mock = mocker.patch('dingdongditch.notifier.notify_by_push')

    notifier.notify('1234', 'asdf1234=', 2)

    notify_by_push_mock.assert_called_with('1234', 'asdf1234=')
    assert not notify_by_phone_mock.called
    assert not log_mock.error.called


def test__notify__recipient_type__unknown(mocker):
    log_mock = mocker.patch('dingdongditch.notifier.logger')
    notify_by_phone_mock = mocker.patch('dingdongditch.notifier.notify_by_phone')
    notify_by_push_mock = mocker.patch('dingdongditch.notifier.notify_by_push')

    result = notifier.notify('1234', 'o hai', 3)

    assert result is False
    assert log_mock.error.called
    assert not notify_by_phone_mock.called
    assert not notify_by_push_mock.called


def test_notify_with_future(mocker):
    executor_mock = mocker.patch('dingdongditch.notifier.executor')

    notifier.notify_with_future('1234', 'asdf1234=', 2)

    executor_mock.submit.assert_called_with(
        notifier.notify,
        '1234',
        'asdf1234=',
        2
    )
