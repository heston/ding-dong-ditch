import atexit
import collections
import datetime
import logging

from blinker import signal
import pyrebase

from . import system_settings as settings

logger = logging.getLogger(__name__)

NAME = 'firebase'
DATABASE_URL = 'https://{}.firebaseio.com'.format(settings.FIREBASE_APP_NAME)
AUTH_DOMAIN = '{}.firebaseapp.com'.format(settings.FIREBASE_APP_NAME)
STORAGE_BUCKET = '{}.appspot.com'.format(settings.FIREBASE_APP_NAME)

firebase_config = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': AUTH_DOMAIN,
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET,
    'serviceAccount': settings.FIREBASE_KEY_PATH,
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()
_streams = {}
_cache = {}

Node = collections.namedtuple('Node', 'value parent key')

def _get_path_list(path):
    path = path.strip('/')

    if path == '':
        return []

    return path.split('/')


class FirebaseData(dict):
    last_updated_at = None
    data_ttl = datetime.timedelta(hours=1)

    def __init__(self, *args, **kwargs):
        self.last_updated_at = datetime.datetime.utcnow()
        super().__init__(*args, **kwargs)

    def get_node_for_path(self, path):
        keys = _get_path_list(path)
        node = self
        p_node = self
        p_key = None

        if not len(keys):
            key = None
        else:
            for key in keys:
                try:
                    new_node = node[key]
                    p_node = node
                    node = new_node
                except KeyError:
                    new_node = {}
                    node[key] = new_node
                    p_node = node
                    node = new_node
                except TypeError:
                    new_node = {}
                    p_new_node = {
                        key: new_node
                    }
                    p_node[p_key] = p_new_node
                    p_node = p_new_node
                    node = new_node
                p_key = key

        return Node(
            value=node,
            parent=p_node,
            key=key
        )

    def set(self, path, data):
        node = self.get_node_for_path(path)
        if not node.key:
            if data is None:
                node.value.clear()
            else:
                node.value.update(data)
        else:
            if data is None:
                del node.parent[node.key]
            else:
                node.parent[node.key] = data

        self.last_updated_at = datetime.datetime.utcnow()
        signal(path).send(self, value=data)

    def merge(self, path, data):
        for rel_path, value in data.items():
            full_path = '{}/{}'.format(path, rel_path)
            self.set(full_path, value)

    def get(self, path):
        parts = _get_path_list(path)
        node = self
        for part in parts:
            try:
                node = node[part]
            except (KeyError, TypeError):
                return None
        return node

    @property
    def is_stale(self):
        if not self.last_updated_at:
            return True

        return datetime.datetime.utcnow() - self.last_updated_at > self.data_ttl


def get_settings():
    try:
        return _cache['user_settings']
    except KeyError:
        # Fetch settings now
        _cache['user_settings'] = FirebaseData(db.child('settings').get().val())
        # Listen for updates
        listen()
        return _cache['user_settings']


def _put_settings_handler(path, data):
    settings = get_settings()
    logger.debug('PUT settings: path=%s data=%s', path, data)
    settings.set(path, data)

def _patch_settings_handler(path, data):
    logger.debug('PATCH settings: path=%s data=%s', path, data)
    settings = get_settings()
    settings.merge(path, data)

def _stream_handler(message):
    logger.debug('STREAM received: %s', message)
    handlers = {
        'put': _put_settings_handler,
        'patch': _patch_settings_handler,
    }
    handler = handlers.get(message['event'])
    if handler:
        handler(message['path'], message['data'])
    else:
        logger.warn('No handler configured for message: %s', message)


def listen():
    _streams['user_settings'] = db.child('settings').stream(_stream_handler)


def set_data(path, data, root='settings'):
    path_list = _get_path_list(path)
    child = db.child(root)
    for path_part in path_list:
        child = child.child(path_part)
    child.set(data)


def reset():
    logger.debug('Resetting all data')
    hangup()
    _cache.clear()


@atexit.register
def hangup():
    logger.debug('Closing all streams')
    for stream in _streams.values():
        stream.close()
