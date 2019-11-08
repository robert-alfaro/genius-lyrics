"""The Genius Lyrics integration."""

import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.components.media_player import (
    ATTR_MEDIA_ARTIST,
    ATTR_MEDIA_TITLE,
)
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_ENTITIES,
    CONF_ENTITY_ID,
    EVENT_HOMEASSISTANT_START,
)

from .const import (
    ATTR_MEDIA_LYRICS,
    DOMAIN,
    SERVICE_SEARCH_LYRICS,
)


_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Optional(CONF_ENTITIES): vol.Any(cv.entity_ids, None),
    })
}, extra=vol.ALLOW_EXTRA)


SERVICE_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(ATTR_MEDIA_ARTIST): cv.string,
        vol.Required(ATTR_MEDIA_TITLE): cv.string,
        vol.Required(CONF_ENTITY_ID): vol.Any(cv.entity_id, None),
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Setup is called when Home Assistant is loading our component."""
    genius_access_token = config[DOMAIN][CONF_ACCESS_TOKEN]

    @callable
    def search_lyrics(call):
        """Handles searching song lyrics."""
        data = call.data
        artist = data[ATTR_MEDIA_ARTIST]
        title = data[ATTR_MEDIA_TITLE]
        entity_id = data.get(CONF_ENTITY_ID)
        state = data.get('state')

        # validate entity_id
        if hass.states.get(entity_id) is None:
            _LOGGER.error(f"entity_id {entity_id} does not exist")
            return False

        # preserve entity's current state
        old_state = hass.states.get(entity_id)
        if old_state:
            attrs = old_state.attributes
        else:
            attrs = {}

        # fetch lyrics
        from .sensor import GeniusLyrics
        genius = GeniusLyrics(genius_access_token)
        genius.fetch_lyrics(artist, title)
        attrs.update({
            ATTR_MEDIA_ARTIST: genius.artist,
            ATTR_MEDIA_TITLE: genius.title,
            ATTR_MEDIA_LYRICS: genius.lyrics,
        })

        # set attributes
        hass.states.async_set(entity_id, state, attrs)

    # register service
    hass.services.async_register(DOMAIN, SERVICE_SEARCH_LYRICS, search_lyrics, SERVICE_SCHEMA)

    # load sensor platform after Home Assistant is started.
    # we need media_player component to be loaded, however, waiting for the
    # media_player component alone may cause problems with entities not existing yet.
    async def load_sensors(event):
        _LOGGER.info(f"Home Assistant is setup..loading sensors")

        # setup platform(s)
        sensor_config = {
            CONF_ACCESS_TOKEN: genius_access_token,
            CONF_ENTITIES: config[DOMAIN][CONF_ENTITIES]
        }
        hass.async_create_task(async_load_platform(hass, 'sensor', DOMAIN, sensor_config, config))

    if config[DOMAIN][CONF_ENTITIES] is not None:
        _LOGGER.info(f"Waiting for HomeAssistant to start before loading sensors")
        hass.bus.async_listen(EVENT_HOMEASSISTANT_START, load_sensors)

    # Return boolean to indicate that initialization was successfully.
    return True
