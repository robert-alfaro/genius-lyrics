"""Helpers for the Genius Lyrics integration"""

import logging


_LOGGER = logging.getLogger(__name__)


def entities_exist(hass, entities):
    """Returns list of entities that exist in hass"""
    exist = []
    for entity in entities:
        if hass.states.get(entity) is None:
            _LOGGER.error(f"entity_id {entity} does not exist")
        else:
            exist.append(entity)
    return exist
