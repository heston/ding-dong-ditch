import atexit
import collections
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


class FirebaseData(dict):
    def _get_path_list(self, path):
        path = path.strip('/')

        if path == '':
            return []

        return path.split('/')

    def get_node_for_path(self, path):
        keys = self._get_path_list(path)
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
            node.value.update(data)
        else:
            node.parent[node.key] = data
        signal(path).send(self, value=data)

    def merge(self, path, data):
        node = self.get_node_for_path(path)
        try:
            node.value.update(data)
            signal(path).send(self, value=data)
        except AttributeError:
            # node is not an updateable type
            raise TypeError(
                'Cannot update path {}. '
                'Existing path points to: {}'.format(path, node.value)
            )

    def get(self, path):
        parts = self._get_path_list(path)
        node = self
        for part in parts:
            try:
                node = node[part]
            except (KeyError, TypeError):
                return None
        return node


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
    logger.debug('PUT settings: path=%s data=%s', path, data)
    _cache['user_settings'].set(path, data)

def _patch_settings_handler(path, data):
    logger.debug('PATCH settings: path=%s data=%s', path, data)
    try:
        _cache['user_settings'].merge(path, data)
    except TypeError as e:
        logger.warn('Cannot update user settings: %s', e)

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


def set_data(path, data):
    req = {
        path: data
    }
    db.child('settings').update(req)


@atexit.register
def hangup():
    for stream in _streams.values():
        stream.close()
