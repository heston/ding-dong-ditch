import pytest

from dingdongditch import system_settings


@pytest.fixture
def settings():
    original_settings = {}

    def setter(**kwargs):
        original_settings.update({k: getattr(system_settings, k) for k in kwargs})
        for k, v in kwargs.items():
            setattr(system_settings, k, v)

    yield setter

    for k, v in original_settings.items():
        setattr(system_settings, k, v)


@pytest.fixture(autouse=True)
def pyfcm(mocker):
    return mocker.patch('pyfcm.FCMNotification')
