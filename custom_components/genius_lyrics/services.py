"""Services for the Genius Lyrics integration."""

from functools import partial
import logging
from typing import Optional

from lyricsgenius import Genius
import voluptuous as vol

from homeassistant.components.media_player import ATTR_MEDIA_ARTIST, ATTR_MEDIA_TITLE
from homeassistant.const import CONF_ENTITY_ID, STATE_OFF, STATE_ON
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
import homeassistant.helpers.config_validation as cv

from .const import (
    ATTR_MEDIA_IMAGE,
    ATTR_MEDIA_LYRICS,
    ATTR_MEDIA_PYONG_COUNT,
    ATTR_MEDIA_STATS_HOT,
    DOMAIN,
    FETCH_RETRIES,
    SERVICE_SEARCH_LYRICS,
)
from .helpers import cleanup_lyrics

_LOGGER = logging.getLogger(__name__)

SERVICE_SEARCH_LYRICS_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(ATTR_MEDIA_ARTIST): cv.string,
                vol.Required(ATTR_MEDIA_TITLE): cv.string,
                vol.Optional(CONF_ENTITY_ID): vol.Any(cv.entity_id, None),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def search_lyrics(
    call: ServiceCall, *, hass: HomeAssistant, genius: Genius
) -> Optional[ServiceResponse]:
    """Service call to handle searching song lyrics."""
    data = call.data
    artist = data.get(ATTR_MEDIA_ARTIST)
    title = data.get(ATTR_MEDIA_TITLE)
    entity_id = data.get(CONF_ENTITY_ID)

    # validate inputs
    if entity_id and hass.states.get(entity_id) is None:
        _LOGGER.error(f"entity_id {entity_id} does not exist")
        return

    if artist is None or title is None:
        _LOGGER.error("Must provide both artist and title")
        return

    attrs = {
        ATTR_MEDIA_ARTIST: artist,
        ATTR_MEDIA_TITLE: title,
        ATTR_MEDIA_LYRICS: None,
        ATTR_MEDIA_IMAGE: None,
        ATTR_MEDIA_PYONG_COUNT: None,
        ATTR_MEDIA_STATS_HOT: None,
    }

    # if entity specified, preserve its current state
    if entity_id:
        old_state = hass.states.get(entity_id)
        if old_state:
            attrs = dict(old_state.attributes)

    # perform fetch
    def fetch_lyrics():
        return genius.search_song(title, artist, get_full_info=False)

    song = await hass.async_add_executor_job(fetch_lyrics)
    if song:
        lyrics = cleanup_lyrics(song)
        attrs.update(
            {
                ATTR_MEDIA_ARTIST: song.artist,
                ATTR_MEDIA_TITLE: song.title,
                ATTR_MEDIA_LYRICS: lyrics,
                ATTR_MEDIA_IMAGE: song.song_art_image_thumbnail_url,
                ATTR_MEDIA_PYONG_COUNT: song.pyongs_count,
                ATTR_MEDIA_STATS_HOT: song.stats.hot,
            }
        )
    else:
        _LOGGER.debug(f"No lyrics found for '{artist} - {title}'")
        attrs[ATTR_MEDIA_LYRICS] = "Lyrics not found"

    # pass media attributes to entity if specified
    # otherwise, return as response.
    if entity_id:
        hass.states.async_set(entity_id, STATE_ON if song else STATE_OFF, attrs)
    else:
        return attrs


@callback
def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the Genius Lyrics integration."""
    # client is shared amongst services
    client = Genius("public", skip_non_songs=True, retries=FETCH_RETRIES)

    hass.services.async_register(
        DOMAIN,
        SERVICE_SEARCH_LYRICS,
        partial(search_lyrics, hass=hass, genius=client),
        schema=SERVICE_SEARCH_LYRICS_SCHEMA,
        supports_response=SupportsResponse.OPTIONAL,
    )
    # TODO: add more services
