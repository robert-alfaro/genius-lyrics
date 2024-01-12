"""The Genius Lyrics integration."""

import logging
import voluptuous as vol

from lyricsgenius import Genius
from requests.exceptions import HTTPError

from homeassistant.core import Event, HomeAssistant, ServiceCall
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
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
    CONF_ACCESS_TOKEN,
    CONF_ENTITIES,
    CONF_ENTITY_ID,
    EVENT_HOMEASSISTANT_START,
)

from .const import (
    ATTR_MEDIA_LYRICS,
    CONF_MONITOR_ALL,
    DATA_GENIUS_CLIENT,
    DOMAIN,
    SERVICE_SEARCH_LYRICS,
    TITLE,
)


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


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Genius Lyrics from a config entry."""

    # access_token = entry.data[CONF_ACCESS_TOKEN]
    monitor_all = entry.data[CONF_MONITOR_ALL]
    selected_entities = entry.data.get(CONF_ENTITIES, [])

    if monitor_all is True:
        # get list of all media_player entities
        monitored_entities = hass.states.async_entity_ids(MP_DOMAIN)
    else:
        monitored_entities = selected_entities

    # any entities to monitor?
    if len(monitored_entities) == 0:
        _err = "No %s entities to monitor", MP_DOMAIN
        _LOGGER.error(_err)
        raise ConfigEntryNotReady(_err)

    # create client object
    genius_client = Genius("public", skip_non_songs=True)

    # # validate access token
    # try:
    #     await hass.async_add_executor_job(genius_client.account)
    # except HTTPError as e:
    #     if e.errno == 401:  # Unauthorized
    #         _LOGGER.error("Failed to authenticate Genius.com access token")
    #         # FIXME: add support for reauth flow step to use below exception
    #         # raise ConfigEntryAuthFailed from e
    #         raise ConfigEntryNotReady from e

    #     raise ConfigEntryError from e

    # stash handle to client object
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        DATA_GENIUS_CLIENT: genius_client
    }

    # store the selected entities in the entry options for later use
    hass.config_entries.async_update_entry(
        entry,
        options={CONF_MONITOR_ALL: monitor_all, CONF_ENTITIES: selected_entities},
    )

    # forward entry setup to platform(s)
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    # set up service(s)
    async def search_lyrics(call: ServiceCall) -> None:
        """Service call to handle searching song lyrics."""
        data = call.data
        artist = data[ATTR_MEDIA_ARTIST]
        title = data[ATTR_MEDIA_TITLE]
        entity_id = data.get(CONF_ENTITY_ID)
        state = data.get("state")

        # validate entity_id
        if hass.states.get(entity_id) is None:
            _LOGGER.error(f"entity_id {entity_id} does not exist")
            return

        # preserve entity's current state
        old_state = hass.states.get(entity_id)
        if old_state:
            attrs = old_state.attributes
        else:
            attrs = {}

        # fetch lyrics
        song = genius_client.search_song(title, artist, get_full_info=False)
        if song:
            attrs.update(
                {
                    ATTR_MEDIA_ARTIST: song.artist,
                    ATTR_MEDIA_TITLE: song.title,
                    ATTR_MEDIA_LYRICS: song.lyrics,
                }
            )

            # set attributes
            hass.states.async_set(entity_id, state, attrs)

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEARCH_LYRICS,
        search_lyrics,
        schema=SERVICE_SEARCH_LYRICS_SCHEMA,
    )

    return True
