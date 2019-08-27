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


def setup(hass, config):
    """setup is called when Home Assistant is loading our component."""
    genius_access_token = config[DOMAIN][CONF_ACCESS_TOKEN]

    def search_lyrics(call):
        """Handle searching for a song's lyrics."""
        data = call.data
        artist = data[ATTR_ARTIST_NAME]
        title = data[ATTR_SONG_TITLE]
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
        #_LOGGER.debug("Searching for lyrics with artist '{}' and title '{}'".format(artist, title))
        song = genius.search_song(title, artist, get_full_info=False)

        if song is None:
            #_LOGGER.debug("Song not found.")
            attrs = {
                'artist': artist.title(),  # title case until we have a preformatted name
                'title' : title,
                'lyrics': None
            }
        else:
            #_LOGGER.debug("Song data: \n{}".format(song.to_dict()))
            attrs = song.to_dict()
            attrs['artist'] = artist.title()  # title case until we have a preformatted name

        if entity_id is not None:
            hass.states.set(entity_id, state, attrs)

    hass.services.register(DOMAIN, 'search_lyrics', search_lyrics)

    # Return boolean to indicate that initialization was successfully.
    return True
