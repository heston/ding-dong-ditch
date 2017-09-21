import atexit
import datetime
import logging
from threading import Timer

DEFAULT_INTERVAL = datetime.timedelta(minutes=30)

_timers = {}
logger = logging.getLogger(__name__)


def watch(name, should_update, update_func, interval=DEFAULT_INTERVAL):
    """Watch something and call a function when it should be updated.

    Arguments:
        should_update: Callable that returns True if the thing being watched
            should be updated, or False otherwise.
        update_func: Callable that updates the thing being watched when {should_update}
            returns True. Watching and updating occurs in a separate thread,
            so ensure this function is threadsafe.
        interval: datetime.timedelta indicating how often to poll {should_update}.

    Returns: A callable that will stop all watchers.
    """

    def start():
        logger.debug('Checking if update is required: %s', should_update)
        _timers[name] = t = Timer(interval.total_seconds(), action)
        t.start()

    def action():
        if should_update():
            logger.debug('Required update detected. Updating: %s', update_func)
            update_func()
        start()

    start()
    return cancel


def cancel(name):
    watcher = _timers.get(name)
    if watcher:
        watcher.cancel()
    del _timers[name]


@atexit.register
def cancel():
    logger.debug('Stopping all watchers')
    for timer in _timers.values():
        timer.cancel()
    _timers.clear()
