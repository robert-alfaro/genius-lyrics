"""The Genius Lyrics integration."""

import json
import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_ENTITY_ID, CONF_ACCESS_TOKEN

_LOGGER = logging.getLogger(__name__)


DOMAIN = 'genius_lyrics'

ATTR_ARTIST_NAME = 'artist_name'
ATTR_SONG_TITLE = 'song_title'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_ACCESS_TOKEN): cv.string
    })
}, extra=vol.ALLOW_EXTRA)

SERVICE_SEARCH_LYRICS = "search_lyrics"
SERVICE_SEARCH_LYRICS = vol.Schema({
    vol.Required(ATTR_ARTIST_NAME): cv.string,
    vol.Required(ATTR_SONG_TITLE): cv.string,
    vol.Optional(CONF_ENTITY_ID): cv.entity_id,
})


def setup(hass, config):
    """setup is called when Home Assistant is loading our component."""
    genius_access_token = config[DOMAIN][CONF_ACCESS_TOKEN]

    def search_lyrics(call):
        """Handle searching for a song's lyrics."""
        data = call.data
        artist = data[ATTR_ARTIST_NAME]
        song = data[ATTR_SONG_TITLE]
        entity_id = data.get(CONF_ENTITY_ID)
        state = data.get("state")
        old_state = hass.states.get(entity_id)
        if old_state:
            attrs = old_state.attributes
        else:
            attrs = {}

        # get lyrics
        from lyricsgenius import Genius
        genius = Genius(genius_access_token)
        song = genius.search_song(song, artist, get_full_info=False)
        #_LOGGER.info("Song data: \n{}".format(song.to_dict()))

        attrs = song.to_dict()
        attrs['artist'] = artist.title()  # title case until we have a preformatted name
        attrs['title'] = attrs['title']

        if entity_id is not None:
            hass.states.set(entity_id, state, attrs)

    hass.services.register(DOMAIN, 'search_lyrics', search_lyrics)

    # Return boolean to indicate that initialization was successfully.
    return True
