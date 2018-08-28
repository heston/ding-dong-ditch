import atexit
import datetime
import os.path

from firebasedata import LiveData
import pyrebase

from . import system_settings as settings

NAME = 'firebase'
DATABASE_URL = 'https://{}.firebaseio.com'.format(settings.FIREBASE_APP_NAME)
AUTH_DOMAIN = '{}.firebaseapp.com'.format(settings.FIREBASE_APP_NAME)
STORAGE_BUCKET = '{}.appspot.com'.format(settings.FIREBASE_APP_NAME)
TTL = datetime.timedelta(hours=2)
ROOT_PATH = '/'
SETTINGS_PATH = '/settings'

firebase_config = {
    'apiKey': settings.FIREBASE_API_KEY,
    'authDomain': AUTH_DOMAIN,
    'databaseURL': DATABASE_URL,
    'storageBucket': STORAGE_BUCKET,
    'serviceAccount': settings.FIREBASE_KEY_PATH,
}

firebase_app = pyrebase.initialize_app(firebase_config)
live_data = LiveData(firebase_app, ROOT_PATH, TTL)


def get_settings():
    return live_data.get_data(SETTINGS_PATH)


def set_data(path, data, root=None):
    default_path = root or SETTINGS_PATH
    abs_path = os.path.join(default_path, path)
    live_data.set_data(abs_path, data)


def reset():
    live_data.reset()


@atexit.register
def hangup():
    live_data.hangup()
