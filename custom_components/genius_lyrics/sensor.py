"""Support for Genius Lyrics sensors."""

import asyncio
import logging

from requests.exceptions import HTTPError, Timeout

from homeassistant.components.media_player import (
    ATTR_MEDIA_ARTIST,
    ATTR_MEDIA_CONTENT_TYPE,
    # ATTR_MEDIA_DURATION,
    ATTR_MEDIA_TITLE,
    MediaType,
)
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_ENTITIES,
    EVENT_HOMEASSISTANT_STARTED,
    STATE_BUFFERING,
    STATE_OFF,
    STATE_ON,
    STATE_PAUSED,
    STATE_PLAYING,
)
from homeassistant.core import CoreState, HomeAssistant, State
from homeassistant.helpers.config_validation import split_entity_id
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change

from .const import (
    ATTR_MEDIA_IMAGE,
    ATTR_MEDIA_LYRICS,
    ATTR_MEDIA_PYONG_COUNT,
    ATTR_MEDIA_STATS_HOT,
    ATTRIBUTION,
    CONF_MONITOR_ALL,
    DOMAIN,
    FETCH_RETRIES,
    INTEGRATION_NAME,
)
from .genius import GeniusPatched
from .helpers import cleanup_lyrics, get_media_player_entities

_LOGGER = logging.getLogger(__name__)


class GeniusLyricsSensor(SensorEntity):
    """Representation of a Genius Lyrics Sensor."""

    _attr_attribution = ATTRIBUTION
    _attr_icon = "mdi:script-text"
    _attr_extra_state_attributes = {}
    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_translation_key = "lyrics"

    def __init__(self, entry: ConfigEntry, media_entity_id) -> None:
        """Initialize the sensor."""
        self._entry = entry
        self._genius = GeniusPatched(
            "public", skip_non_songs=True, retries=FETCH_RETRIES
        )
        self._media_player_id = media_entity_id

        media_player_name = split_entity_id(media_entity_id)[1]
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
        self._attr_device_info = DeviceInfo(
            configuration_url="https://www.genius.com/",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, self._entry.entry_id)},
            manufacturer=INTEGRATION_NAME,
            name=INTEGRATION_NAME,
        )

        self.reset(update=False)
        _LOGGER.info("Created sensor: %s", self._attr_name)

    def reset(self, update=True):
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
        if update:
            self.async_schedule_update_ha_state(True)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def _fetch_lyrics(self) -> bool:
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

            # hack cleanup of lyrics to remove erroneous text
            lyrics = cleanup_lyrics(song)

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
            try:
                self._fetch_lyrics()
            except Timeout:
                _LOGGER.error(
                    f"Timeout fetching lyrics ({self._genius.retries} retries)"
                )
            except HTTPError as e:
                _LOGGER.error(
                    f"HTTP error fetching lyrics ({self._genius.retries} retries), err: {e.strerror}"
                )
            else:
                return

            # on exception only
            self.reset()

    async def handle_state_change(
        self, entity_id: str, old_state: State, new_state: State
    ):
        """Handle media player state changes to trigger new search."""

        # ensure tracking correct entity_id
        if entity_id != self._media_player_id:
            return

        if new_state is None:
            _LOGGER.debug(
                f"Detected removed or disabled entity: {entity_id}, new_state is None"
            )
            # do nothing...entity registry handler manages real changes
            self.reset()
            return

        # ensure a state containing necessary query inputs
        if new_state.state not in [STATE_PLAYING, STATE_PAUSED, STATE_BUFFERING]:
            self.reset()
            return

        # bail if not playing music content type
        content_type = new_state.attributes.get(ATTR_MEDIA_CONTENT_TYPE)
        if content_type != MediaType.MUSIC:
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

        # trigger search via update
        self.async_schedule_update_ha_state(True)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Genius Lyrics sensor based on a config entry."""

    # on startup, entry setup is delayed until HA START event
    # otherwise, proceed immediately.
    startup_event = asyncio.Event()

    async def startup_callback(event):
        _LOGGER.info("Home Assistant is started..loading sensors")
        startup_event.set()  # set the event to signal that Home Assistant is started

    if hass.state == CoreState.starting:
        _LOGGER.info("Waiting for HomeAssistant to start before loading sensors")
        hass.bus.async_listen(EVENT_HOMEASSISTANT_STARTED, startup_callback)
        await startup_event.wait()

    # SETUP ENTRY START

    monitor_all = entry.options[CONF_MONITOR_ALL]

    if monitor_all is True:
        # get list of all media_player entities
        monitored_entities = get_media_player_entities(hass)
    else:
        # get list of user-selected media_player entities
        monitored_entities = entry.options[CONF_ENTITIES]

    # create sensors, one for each monitored entity
    sensors = []
    for media_player in monitored_entities:
        _LOGGER.debug(f"Creating sensor to monitor {media_player}")

        # create new sensor & hook up to media_player
        genius_sensor = GeniusLyricsSensor(entry, media_player)
        async_track_state_change(hass, media_player, genius_sensor.handle_state_change)

        sensors.append(genius_sensor)

    # add new sensors
    async_add_entities(sensors)
