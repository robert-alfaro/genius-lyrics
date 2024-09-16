"""Helpers for the Genius Lyrics integration."""

import logging
import re

from lyricsgenius.song import Song

from homeassistant.components.media_player import DOMAIN as MP_DOMAIN
from homeassistant.const import ATTR_RESTORED
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


def clean_song_title(song_title):
    """Clean song title string by removing metadata that may appear."""

    # Keywords to look for in parentheses, brackets, or after a hyphen
    keywords = r"(remaster(?:ed)?|anniversary|instrumental|live|edit(?:ion)?|single(s)?|stereo|album|radio|version|feat(?:uring)?|mix|bonus)"

    # Regex pattern to match metadata within parentheses or brackets
    paren_bracket_pattern = rf"[\(\[][^\)\]]*\b({keywords})\b[^\)\]]*[\)\]]"
    cleaned_title = re.sub(paren_bracket_pattern, "", song_title, flags=re.IGNORECASE)

    # Regex pattern to match a hyphen followed by metadata (keywords or a year)
    hyphen_pattern = rf"(\s*-\s*(\d{{4}}|{keywords}).*)$"
    cleaned_title = re.sub(hyphen_pattern, "", cleaned_title, flags=re.IGNORECASE)

    # Remove any dangling hyphens or extra spaces
    cleaned_title = re.sub(r"\s*-\s*$", "", cleaned_title).strip()

    # Remove any leftover unmatched parentheses or brackets
    cleaned_title = re.sub(r"\s[\(\[\{\]\)\}\s]+$", "", cleaned_title).strip()

    return cleaned_title


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
