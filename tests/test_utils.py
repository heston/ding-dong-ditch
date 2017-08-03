import pytest

from dingdongditch.utils import Env


@pytest.fixture
def getenv(mocker):
    return mocker.patch('os.getenv')


def test_raw__with_env(getenv):
    getenv.return_value = 'baz'

    result = Env.raw('foo')

    getenv.assert_called_with('foo', None)
    assert result == 'baz'


def test_raw__with_default(getenv):
    result = Env.raw('foo', 'bar')

    getenv.assert_called_with('foo', 'bar')


def test_string(getenv):
    getenv.return_value = 'foo'

    result = Env.string('FOO')

    assert result == 'foo'


def test_number__int(getenv):
    getenv.return_value = '1234'

    result = Env.number('FOO')

    assert result == 1234


def test_number__float(getenv):
    getenv.return_value = '1234.5678'

    result = Env.number('FOO')

    assert result == 1234.5678


def test_number__boolean__string(getenv):
    getenv.return_value = 'foo'

    result = Env.boolean('FOO')

    assert result is True


def test_number__boolean__empty(getenv):
    getenv.return_value = ''

    result = Env.boolean('FOO')

    assert result is False


def test_number__boolean__0(getenv):
    getenv.return_value = '0'

    result = Env.boolean('FOO')

    assert result is False


def test_number__boolean__false(getenv):
    getenv.return_value = 'false'

    result = Env.boolean('FOO')

    assert result is False


def test_number__boolean__False(getenv):
    getenv.return_value = 'False'

    result = Env.boolean('FOO')

    assert result is False


def test_number__boolean__off(getenv):
    getenv.return_value = 'off'

    result = Env.boolean('FOO')

    assert result is False


def test_number__boolean__no(getenv):
    getenv.return_value = 'no'

    result = Env.boolean('FOO')

    assert result is False
