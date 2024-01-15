"""Helpers for the Genius Lyrics integration."""

import logging
import re
from lyricsgenius.song import Song

_LOGGER = logging.getLogger(__name__)


def entities_exist(hass, entities):
    """Return list of entities that exist in hass."""
    exist = []
    for entity in entities:
        if hass.states.get(entity) is None:
            _LOGGER.error(f"entity_id {entity} does not exist")
        else:
            exist.append(entity)
    return exist


def cleanup_lyrics(song: Song) -> str:
    """Clean lyrics string hackishly remove erroneous text that may appear."""

    # Pattern1: match digits at beginning followed by "Contributors" and text followed by "Lyrics"
    pattern1 = re.compile(r"^(\d+) Contributors(.*?) Lyrics")
    match = pattern1.match(song.lyrics)
    if match:
        # Remove the matched patterns from the original text
        lyrics = song.lyrics.replace(match.group(0), "")

    # Pattern2: match ending with "Embed"
    lyrics = lyrics.rstrip("Embed")

    # Pattern3: match ending with Pyong Count
    lyrics = lyrics.rstrip(str(song.pyongs_count))

    return lyrics
