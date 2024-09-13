"""The Genius Lyrics integration."""

import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_RESTORED,
    CONF_ACCESS_TOKEN,
    CONF_ENTITIES,
    Platform,
)
from homeassistant.core import Event, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import split_entity_id
import homeassistant.helpers.entity_registry as er
from homeassistant.helpers.entity_registry import (
    EVENT_ENTITY_REGISTRY_UPDATED,
    RegistryEntryDisabler,
)
from homeassistant.helpers.network import get_url

from .const import CONF_MONITOR_ALL, DOMAIN, INTEGRATION_NAME
from .helpers import get_media_player_entities
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)


async def async_notify_user(hass: HomeAssistant, message: str) -> None:
    """Notify the user with a persistent notification."""
    data = {
        "title": INTEGRATION_NAME,
        "message": message,
    }
    await hass.services.async_call("persistent_notification", "create", data)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Genius Lyrics from a config entry."""

    # prefer options
    if CONF_MONITOR_ALL in entry.options:
        monitor_all = entry.options[CONF_MONITOR_ALL]
    else:
        monitor_all = entry.data[CONF_MONITOR_ALL]

    if monitor_all is True:
        monitored_entities = get_media_player_entities(hass)
        user_selected_entities = []
    else:
        user_selected_entities = (
            entry.options[CONF_ENTITIES]
            if CONF_ENTITIES in entry.options
            else entry.data[CONF_ENTITIES]
        )
        monitored_entities = user_selected_entities

    # store options
    hass.config_entries.async_update_entry(
        entry,
        options={CONF_MONITOR_ALL: monitor_all, CONF_ENTITIES: user_selected_entities},
    )

    # any entities to monitor?
    if len(monitored_entities) == 0:
        _err = f"No {Platform.MEDIA_PLAYER} entities to monitor"
        _LOGGER.error(_err)
        raise ConfigEntryNotReady(_err)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}

    # listen for options updates
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # forward entry setup to platform(s)
    await hass.config_entries.async_forward_entry_setup(entry, Platform.SENSOR)

    # track entity registry to detect new/removed media_player entities
    async def handle_entity_registry_update(event: Event) -> None:
        """Handle addition/removal of a media_player entities."""

        entity_id = event.data["entity_id"]
        entity_domain, entity_name = split_entity_id(entity_id)
        if entity_domain != Platform.MEDIA_PLAYER:
            return

        sensor_entity_id = f"{Platform.SENSOR}.{entity_name}_lyrics"
        registry = er.async_get(hass)
        action = event.data["action"]

        if action == "create":
            # trigger reload if monitoring all media_player entities
            # otherwise, issue notification about event.
            if monitor_all is True:
                _LOGGER.debug(
                    f"New {Platform.MEDIA_PLAYER} detected: {entity_name}, reloading..."
                )
                await async_reload_entry(hass, entry)
                sensor_url = (
                    f"{get_url(hass)}/config/entities?config_entry={entry.entry_id}"
                )
                notify_link = f"Auto-configured {sensor_entity_id}, <a href='{sensor_url}'>Check it out</a>."
            else:
                _LOGGER.debug(f"Ignoring new {Platform.MEDIA_PLAYER}: {entity_name}")
                integration_url = (
                    f"{get_url(hass)}/config/integrations/integration/{DOMAIN}"
                )
                notify_link = f"<a href='{integration_url}'>Configure</a> {entity_id}."

            await async_notify_user(
                hass,
                f"Detected new media player! {notify_link}",
            )

        elif action == "remove":
            # remove sensor for a monitored media_player entity
            if monitor_all is True or entity_id in monitored_entities:
                _LOGGER.info(f"Removing sensor for {entity_id}")

                registry = er.async_get(hass)
                try:
                    registry.async_remove(sensor_entity_id)
                except KeyError:
                    _LOGGER.warning("Sensor already removed")

                # cleanup entity with restored state
                state = hass.states.get(sensor_entity_id)
                if state and state.attributes.get(ATTR_RESTORED):
                    if hass.states.async_remove(
                        sensor_entity_id, context=event.context
                    ):
                        _LOGGER.debug(
                            f"Successfully removed restored entity: {sensor_entity_id}"
                        )
                    else:
                        _LOGGER.error(
                            f"Failed to remove restored entity: {sensor_entity_id}"
                        )

                # remove entity from options list if media_player was user-selected
                if monitor_all is False:
                    monitored_entities.remove(entity_id)
                    hass.config_entries.async_update_entry(
                        entry,
                        options={
                            CONF_MONITOR_ALL: monitor_all,
                            CONF_ENTITIES: monitored_entities,
                        },
                    )

                # trigger reload
                await async_reload_entry(hass, entry)

        elif action == "update":
            # adjust sensor enabled state per monitored media_player enabled state
            mp_entry = registry.async_get(entity_id)
            if mp_entry and (monitor_all is True or entity_id in monitored_entities):
                # only update entity when disabled statuses differs
                sensor_entry = registry.async_get(sensor_entity_id)
                if sensor_entry is not None and (
                    sensor_entry.disabled != mp_entry.disabled
                ):
                    _LOGGER.info(
                        f"Auto-{'disabling' if mp_entry.disabled else 'enabling'} sensor per {entity_id}"
                    )
                    registry.async_update_entity(
                        sensor_entity_id,
                        disabled_by=RegistryEntryDisabler.INTEGRATION
                        if mp_entry.disabled
                        else None,
                    )

    hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, handle_entity_registry_update)

    # set up services
    async_setup_services(hass)

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle an options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Genius Lyrics config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, [Platform.SENSOR]
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
