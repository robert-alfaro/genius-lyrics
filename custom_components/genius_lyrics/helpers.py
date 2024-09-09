"""Helpers for the Genius Lyrics integration."""

import logging
from lyricsgenius.song import Song
from re import compile as re_compile
from re import sub as re_sub

from homeassistant.core import HomeAssistant
from homeassistant.const import ATTR_RESTORED
from homeassistant.components.media_player import DOMAIN as MP_DOMAIN

_LOGGER = logging.getLogger(__name__)


def cleanup_lyrics(song: Song) -> str:
    """Clean lyrics string hackishly remove erroneous text that may appear."""

    # Pattern1: match digits at beginning followed by "Contributors" and text followed by "Lyrics"
    pattern1 = re_compile(r"^(\d+) Contributors(.*?) Lyrics")
    match = pattern1.match(song.lyrics)
    if match:
        # Remove the matched patterns from the original text
        lyrics = song.lyrics.replace(match.group(0), "")

    # Pattern2: match ending with "Embed"
    lyrics = lyrics.rstrip("Embed")

    # Pattern3: match ending with Pyong Count
    lyrics = lyrics.rstrip(str(song.pyongs_count))
    
    # Pattern4: remove 'You might also like'
    lyrics = lyrics.replace("You might also like[","[")
    
    # Pattern5: remove live ticket advertising
    deletetxt = "See " + song.artist + " LiveGet tickets as low as "
    lyrics = lyrics.replace(deletetxt, "")
    lyrics = re_sub("\$[0-9]*\[","[", lyrics)

    return lyrics


def get_media_player_entities(hass: HomeAssistant, ignore_restored: bool = True):
    """Return list of media_player entity ids."""
    mp_entity_ids = []
    entity_ids = hass.states.async_entity_ids(MP_DOMAIN)

    for entity_id in entity_ids:
        state = hass.states.get(entity_id)
        if ignore_restored and state.attributes.get(ATTR_RESTORED):
            _LOGGER.debug(f"Ignoring restored entity: {entity_id}")
            continue
        mp_entity_ids.append(entity_id)

    return mp_entity_ids
