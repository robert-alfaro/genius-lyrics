"""Sensor platform for the Genius Lyrics integration."""

import asyncio
import logging
import re
import voluptuous as vol
from lyricsgenius import Genius

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import CoreState, HomeAssistant, State
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import entities_domain, split_entity_id
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change
from homeassistant.exceptions import PlatformNotReady
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_ENTITIES,
    EVENT_HOMEASSISTANT_STARTED,
    STATE_ON,
    STATE_OFF,
    STATE_PLAYING,
    STATE_PAUSED,
    STATE_BUFFERING,
)
from homeassistant.components.media_player import (
    ATTR_MEDIA_CONTENT_TYPE,
    ATTR_MEDIA_DURATION,
    ATTR_MEDIA_TITLE,
    ATTR_MEDIA_ARTIST,
    DOMAIN as MP_DOMAIN,
)
from homeassistant.components.media_player.const import MEDIA_TYPE_MUSIC

from .const import (
    ATTRIBUTION,
    ATTR_MEDIA_LYRICS,
    ATTR_MEDIA_IMAGE,
    ATTR_MEDIA_PYONG_COUNT,
    ATTR_MEDIA_STATS_HOT,
    CONF_MONITOR_ALL,
    DATA_GENIUS_CLIENT,
    DOMAIN,
)

from .helpers import (
    entities_exist,
)

_LOGGER = logging.getLogger(__name__)


class GeniusLyricsSensor(SensorEntity):
    """Representation of a Genius Lyrics Sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_icon = "mdi:script-text"
    _attr_extra_state_attributes = {}
    _attr_should_poll = False
    _attr_has_entity_name = True
    __state = STATE_OFF
    _attr_translation_key = "lyrics"

    def __init__(self, entry: ConfigEntry, media_entity_id) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._genius = Genius("public", skip_non_songs=True)
        self._media_player_id = media_entity_id

        media_player_name = split_entity_id(media_entity_id)[1]
        # cleaned_name = _media_player_name.split("_")
        # cleaned_name = " ".join([str(s).capitalize() for s in cleaned_name])
        cleaned_name = media_player_name.replace("_", " ").capitalize()
        self._attr_name = f"{cleaned_name} lyrics"

        self._attr_unique_id = "_".join(
            [
                DOMAIN,
                media_player_name,
                "sensor",
                "lyrics",
            ]
        )

        self.reset()

        _LOGGER.info("Created sensor: %s", self._attr_name)

    def reset(self):
        """Reset sensor state and attributes."""
        self._media_artist = None
        self._media_title = None
        self._state = STATE_OFF
        self._attr_entity_picture = None
        self._attr_extra_state_attributes[ATTR_MEDIA_ARTIST] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_TITLE] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_LYRICS] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_IMAGE] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_PYONG_COUNT] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_STATS_HOT] = None
        _LOGGER.debug("Sensor data is now reset")

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def _fetch_lyrics(self):
        if self._media_artist is None or self._media_title is None:
            _LOGGER.error("Cannot fetch lyrics without artist and title")
            return

        _LOGGER.info(
            "Searching lyrics for artist='%s' and title='%s'",
            self._media_artist,
            self._media_title,
        )

        self._attr_extra_state_attributes[ATTR_MEDIA_ARTIST] = self._media_artist
        self._attr_extra_state_attributes[ATTR_MEDIA_TITLE] = self._media_title

        song = self._genius.search_song(
            self._media_title, self._media_artist, get_full_info=False
        )
        if song:
            _LOGGER.debug(
                "Found song: artist = %s, title = %s", song.artist, song.title
            )

            self._media_title = song.title
            lyrics = song.lyrics

            # HACK: clean up results

            # Pattern1: match digits at beginning followed by "Contributors" and text followed by "Lyrics"
            pattern1 = re.compile(r"^(\d+) Contributors(.*?) Lyrics")
            match = pattern1.match(song.lyrics)
            if match:
                # Remove the matched patterns from the original text
                lyrics = lyrics.replace(match.group(0), "")

            # Pattern2: match ending with "Embed"
            lyrics = lyrics.rstrip("Embed")

            # Pattern3: match ending with Pyong Count
            lyrics = lyrics.rstrip(str(song.pyongs_count))

            # end HACK

            self._attr_extra_state_attributes[ATTR_MEDIA_LYRICS] = lyrics
            self._attr_extra_state_attributes[ATTR_MEDIA_STATS_HOT] = song.stats.hot
            self._attr_extra_state_attributes[
                ATTR_MEDIA_PYONG_COUNT
            ] = song.pyongs_count
            self._attr_extra_state_attributes[
                ATTR_MEDIA_IMAGE
            ] = song.song_art_image_thumbnail_url
            self._attr_entity_picture = song.song_art_image_thumbnail_url
            self._state = STATE_ON
            return True

        self._attr_extra_state_attributes[ATTR_MEDIA_LYRICS] = "Lyrics not found"
        self._attr_extra_state_attributes[ATTR_MEDIA_IMAGE] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_STATS_HOT] = None
        self._attr_extra_state_attributes[ATTR_MEDIA_PYONG_COUNT] = None
        self._attr_entity_picture = None
        self._state = STATE_OFF
        return False

    def update(self):
        """Fetch new state data for the sensor."""
        if self.state == STATE_ON:
            self._fetch_lyrics()

    async def handle_state_change(
        self, entity_id: str, old_state: State, new_state: State
    ):
        """Handle media player state changes to trigger new search."""

        # ensure tracking correct entity_id
        if entity_id != self._media_player_id:
            return

        # ensure a state containing necessary query inputs
        if new_state.state not in [STATE_PLAYING, STATE_PAUSED, STATE_BUFFERING]:
            self.reset()
            self.async_schedule_update_ha_state(True)
            return

        # bail if not playing music content type
        content_type = new_state.attributes.get(ATTR_MEDIA_CONTENT_TYPE)
        if content_type != MEDIA_TYPE_MUSIC:
            _LOGGER.warning(f"Ignoring non-music content type: {content_type}")
            return

        # TODO: need to check duration? new_state.attributes.get(ATTR_MEDIA_DURATION)

        # bail if media title has not changed
        if self._media_title == new_state.attributes.get(ATTR_MEDIA_TITLE):
            _LOGGER.debug("Media title has not changed")
            return

        # all checks out..update artist and title to fetch
        self._media_artist = new_state.attributes.get(ATTR_MEDIA_ARTIST)
        self._media_title = new_state.attributes.get(ATTR_MEDIA_TITLE)
        self._attr_extra_state_attributes[ATTR_MEDIA_LYRICS] = None
        self._attr_entity_picture = None
        self._state = STATE_ON

        # trigger update
        self.async_schedule_update_ha_state(True)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Genius Lyrics sensor based on a config entry."""

    startup_event = asyncio.Event()

    # on startup, entry setup is delayed until HA START event
    # otherwise, proceed immediately.

    async def startup_callback(event):
        _LOGGER.info("Home Assistant is started..loading sensors")
        startup_event.set()  # set the event to signal that Home Assistant is started

    if hass.state == CoreState.starting:
        _LOGGER.info("Waiting for HomeAssistant to start before loading sensors")
        hass.bus.async_listen(EVENT_HOMEASSISTANT_STARTED, startup_callback)
        await startup_event.wait()

    # SETUP ENTRY START

    # genius_client = hass.data[DOMAIN][entry.entry_id][DATA_GENIUS_CLIENT]

    if entry.data[CONF_MONITOR_ALL] is True:
        # get list of all media_player entities
        monitored_entities = hass.states.async_entity_ids(MP_DOMAIN)
    else:
        # get list of user-selected media_player entities
        monitored_entities = entry.data[CONF_ENTITIES]

    # create sensors, one for each monitored entity
    sensors = []
    for media_player in monitored_entities:
        _LOGGER.info(f"Creating sensor to monitor {media_player}")

        # check if sensor already created?
        entity_name = f"{split_entity_id(media_player)[1]}_lyrics"
        if hass.states.get(entity_name) is not None:
            _LOGGER.warning(f"Sensor already exists: {entity_name}")
            continue

        # create new sensor & hook up to media_player
        genius_sensor = GeniusLyricsSensor(entry, media_player)
        async_track_state_change(hass, media_player, genius_sensor.handle_state_change)

        sensors.append(genius_sensor)

    # add new sensors
    async_add_entities(sensors)
