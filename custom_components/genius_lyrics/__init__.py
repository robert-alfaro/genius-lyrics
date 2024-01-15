"""The Genius Lyrics integration."""

import logging
import voluptuous as vol

from lyricsgenius import Genius
from requests.exceptions import HTTPError

from homeassistant.core import Event, HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import split_entity_id
import homeassistant.helpers.entity_registry as er
from homeassistant.helpers.entity_registry import EVENT_ENTITY_REGISTRY_UPDATED
from homeassistant.helpers.network import get_url
from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    ConfigEntryError,
    ConfigEntryNotReady,
)
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.components.media_player import (
    ATTR_MEDIA_ARTIST,
    ATTR_MEDIA_TITLE,
    DOMAIN as MP_DOMAIN,
)
from homeassistant.const import (
    ATTR_RESTORED,
    CONF_ACCESS_TOKEN,
    CONF_ENTITIES,
    CONF_ENTITY_ID,
    EVENT_HOMEASSISTANT_START,
    STATE_ON,
    STATE_OFF,
)

from .const import (
    ATTR_MEDIA_LYRICS,
    ATTR_MEDIA_IMAGE,
    ATTR_MEDIA_PYONG_COUNT,
    ATTR_MEDIA_STATS_HOT,
    CONF_MONITOR_ALL,
    DATA_GENIUS_CLIENT,
    DOMAIN,
    FETCH_RETRIES,
    SERVICE_SEARCH_LYRICS,
    INTEGRATION_NAME,
)
from .helpers import cleanup_lyrics

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_ACCESS_TOKEN): cv.string,
                vol.Optional(CONF_ENTITIES): vol.Any(cv.entity_ids, None),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


SERVICE_SEARCH_LYRICS_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(ATTR_MEDIA_ARTIST): cv.string,
                vol.Required(ATTR_MEDIA_TITLE): cv.string,
                vol.Required(CONF_ENTITY_ID): vol.Any(cv.entity_id, None),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def notify_user(hass: HomeAssistant, message: str) -> None:
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
        monitored_entities = hass.states.async_entity_ids(MP_DOMAIN)
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
        _err = f"No {MP_DOMAIN} entities to monitor"
        _LOGGER.error(_err)
        raise ConfigEntryNotReady(_err)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}

    # listen for options updates
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # forward entry setup to platform(s)
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    # track entity registry to detect new/removed media_player entities
    async def handle_entity_registry_update(event: Event) -> None:
        """Handle addition/removal of a media_player entities."""

        entity_id = event.data["entity_id"]
        entity_domain, entity_name = split_entity_id(entity_id)
        if entity_domain != MP_DOMAIN:
            return

        action = event.data["action"]
        if action == "create":
            # trigger reload if monitoring all media_player entities
            # otherwise, issue notification about event.
            if monitor_all is True:
                _LOGGER.debug(f"New {MP_DOMAIN} detected: {entity_name}, reloading...")
                await async_reload_entry(hass, entry)
            else:
                _LOGGER.debug(f"Ignoring new {MP_DOMAIN}: {entity_name}")
                integration_url = (
                    f"{get_url(hass)}/config/integrations/integration/{DOMAIN}"
                )
                await notify_user(
                    hass,
                    f"Detected new media player! "
                    f"<a href='{integration_url}'>Configure</a> {entity_id}.",
                )

        elif action == "remove":
            # remove sensor for a monitored media_player entity
            if monitor_all is True or entity_id in monitored_entities:
                _LOGGER.debug(f"Removing sensor for {entity_id}")
                sensor_entity_id = f"sensor.{entity_name}_lyrics"

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
                        _LOGGER.warning(
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

    hass.bus.async_listen(EVENT_ENTITY_REGISTRY_UPDATED, handle_entity_registry_update)

    # set up service(s)

    # create shared client for services
    genius_client = Genius("public", skip_non_songs=True, retries=FETCH_RETRIES)

    async def search_lyrics(call: ServiceCall) -> None:
        """Service call to handle searching song lyrics."""
        data = call.data
        artist = data.get(ATTR_MEDIA_ARTIST)
        title = data.get(ATTR_MEDIA_TITLE)
        entity_id = data.get(CONF_ENTITY_ID)

        # validate inputs
        if hass.states.get(entity_id) is None:
            _LOGGER.error(f"entity_id {entity_id} does not exist")
            return

        if artist is None or title is None:
            _LOGGER.error("Must provide both artist and title")
            return

        # preserve entity's current state
        old_state = hass.states.get(entity_id)
        if old_state:
            attrs = dict(old_state.attributes)
        else:
            attrs = {}

        # perform fetch
        def fetch_lyrics():
            return genius_client.search_song(title, artist, get_full_info=False)

        song = await hass.async_add_executor_job(fetch_lyrics)
        if song:
            lyrics = cleanup_lyrics(song)
            attrs.update(
                {
                    ATTR_MEDIA_ARTIST: song.artist,
                    ATTR_MEDIA_TITLE: song.title,
                    ATTR_MEDIA_LYRICS: lyrics,
                    ATTR_MEDIA_IMAGE: song.song_art_image_url,
                    ATTR_MEDIA_PYONG_COUNT: song.pyongs_count,
                    ATTR_MEDIA_STATS_HOT: song.stats.hot,
                }
            )

            # set media attributes on entity
            hass.states.async_set(entity_id, STATE_ON, attrs)
        else:
            _LOGGER.error(f"No lyrics found for '{artist} - {title}'")

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEARCH_LYRICS,
        search_lyrics,
        schema=SERVICE_SEARCH_LYRICS_SCHEMA,
    )

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle an options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Genius Lyrics config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
