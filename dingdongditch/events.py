import datetime
import hashlib
import logging

from . import user_settings

logger = logging.getLogger(__name__)

EVENT_NONCE = 'DDD-EVENT'
DEFAULT_EVENT_NAME = 'doorbell'
EVENT_ROOT = 'events'


def get_event_id():
    now = datetime.datetime.utcnow()
    digest = hashlib.sha256()
    digest.update(EVENT_NONCE.encode('utf-8'))
    digest.update(str(datetime.datetime.utcnow().timestamp()).encode('utf-8'))
    return digest.hexdigest()


def get_event_path(unit_id, event_id):
    return '{}/{}'.format(unit_id, event_id)


def record_event(unit_id, event_name=None):
    if not unit_id:
        return

    event_id = get_event_id()
    event_path = get_event_path(unit_id, event_id)
    event_payload = {
        'name': event_name or DEFAULT_EVENT_NAME
    }
    logger.info('Recording event "%s" for unit %s', event_id, unit_id)
    user_settings.set_data(event_path, event_payload, root='events')
    return event_id
