import logging
import time
import uuid

from . import user_settings

logger = logging.getLogger(__name__)

DEFAULT_EVENT_NAME = 'doorbell'
EVENT_ROOT = 'events'


def get_event_id():
    return str(uuid.uuid4())


def get_event_path(unit_id, event_id):
    return '{}/{}'.format(unit_id, event_id)


def record_event(unit_id, event_name=None):
    if not unit_id:
        return

    event_id = get_event_id()
    event_path = get_event_path(unit_id, event_id)
    event_payload = {
        'name': event_name or DEFAULT_EVENT_NAME,
        'occurredAt': time.time(),
    }
    logger.info('Recording event "%s" for unit %s', event_id, unit_id)
    user_settings.set_data(event_path, event_payload, root=EVENT_ROOT)
    return event_id
