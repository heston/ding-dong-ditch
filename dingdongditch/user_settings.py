from collections import namedtuple
from datetime import datetime, timedelta
import logging
import os.path
import pickle

from . import system_settings as settings
from . import firebase_user_settings_adapter

ADAPTERS = {
    'firebase': firebase_user_settings_adapter
}

logger = logging.getLogger(__name__)

Unit = namedtuple('Unit', 'should_ring_bell recipients')


def get_data():
    adapter_name = settings.USER_SETTINGS_ADAPTER
    if adapter_name not in ADAPTERS:
        raise ValueError('Unknown adapter: {}'.format(adapter_name))

    logger.info('Getting user settings from adapter "%s"', adapter_name)

    try:
        data = ADAPTERS[adapter_name].get_settings()
    except Exception as e:
        logger.exception(
            'Could not load user settings from adapter "%s": %s', adapter_name, e
        )
        return None
    return data


def get_unit_by_id(unit_id):
    """
    Return a Unit by its ID.
    """
    # Keys should always be strings
    unit_id = str(unit_id)
    data = get_data()
    if data and unit_id in data:
        unit_data = data[unit_id]
        should_ring_bell = unit_data.get('chime', 1)
        recipients = list(unit_data.get('recipients', {}).keys())
        return Unit(
            should_ring_bell=should_ring_bell,
            recipients=recipients
        )
    return None
