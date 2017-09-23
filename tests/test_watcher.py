from datetime import timedelta
import time

from dingdongditch import watcher


def test_watcher__not_stale(mocker):
    is_stale = mocker.Mock()
    is_stale.side_effect = [
        False,
        False,
        False,
    ]
    update = mocker.Mock()
    interval = timedelta(seconds=.001)
    watcher.watch('test_watcher', is_stale, update, interval)
    time.sleep(.1)
    watcher.cancel('test_watcher')
    assert is_stale.call_count == 4
    assert update.called is False


def test_watcher__stale(mocker):
    is_stale = mocker.Mock()
    is_stale.side_effect = [
        False,
        False,
        True,
    ]
    update = mocker.Mock()
    interval = timedelta(seconds=.001)
    watcher.watch('test_watcher', is_stale, update, interval)
    time.sleep(.1)
    watcher.cancel('test_watcher')
    assert is_stale.call_count == 4
    assert update.called is True
