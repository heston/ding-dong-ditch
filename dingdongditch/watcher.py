import atexit
import datetime
import logging
from threading import Timer

DEFAULT_INTERVAL = datetime.timedelta(minutes=30)

_watchers = {}
logger = logging.getLogger(__name__)


class Watcher:
    def __init__(self, should_update, update_func, interval=None):
        self.should_update = should_update
        self.update_func = update_func
        self.interval = DEFAULT_INTERVAL if interval is None else interval
        self.running = False

    def start(self):
        self.should_cancel = False
        self._timer = Timer(self.interval.total_seconds(), self._action)
        self._timer.start()
        self.running = True

    def _action(self):
        if self.should_cancel:
            self.running = False
            return

        logger.debug('Checking if update is required: %s', self.should_update)
        if self.should_update():
            logger.debug('Required update detected. Updating: %s', self.update_func)
            self.update_func()
        # Start a new timer
        self.start()

    def cancel(self):
        self.should_cancel = True


def watch(name, should_update, update_func, interval=None):
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
    watcher = Watcher(should_update, update_func, interval)
    _watchers[name] = watcher
    watcher.start()


def cancel(name):
    if name not in _watchers:
        return None
    logger.debug('Stopping watcher %s', name)
    watcher = _watchers[name]
    if watcher:
        watcher.cancel()
    del _watchers[name]
    return True


@atexit.register
def cancel_all():
    logger.debug('Stopping all watchers')
    for watcher in _watchers.values():
        watcher.cancel()
    _watchers.clear()
