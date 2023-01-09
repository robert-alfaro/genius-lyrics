"""Sensor platform for the Genius Lyrics integration."""

import logging

import voluptuous as vol
from homeassistant.helpers.config_validation import entities_domain, split_entity_id
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_ENTITIES,
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
)
from homeassistant.components.media_player.const import MEDIA_TYPE_MUSIC

from .const import (
    ATTR_MEDIA_LYRICS,
)

from .helpers import (
    entities_exist,
)


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    if discovery_info is None:
        return

    access_token = discovery_info.get(CONF_ACCESS_TOKEN)
    conf_entities = discovery_info.get(CONF_ENTITIES)

    # validate the entities exist
    monitored_entities = entities_exist(hass, conf_entities)

    # ensure we've got at least one entity to monitor
    if not len(monitored_entities):
        _LOGGER.error("No valid entities to monitor")
        return False

    # validate entities are part of media_player domain
    try:
        validate_entities = entities_domain('media_player')
        validate_entities(conf_entities)
    except vol.Invalid as e:
        _LOGGER.error(e)
        return False
    else:
        _LOGGER.debug(f"Monitoring media players: {monitored_entities}")

    # create sensors, one for each monitored entity
    genius = GeniusLyrics(access_token)
    sensors = []
    for media_player in monitored_entities:
        # create sensor
        genius_sensor = GeniusLyricsSensor(hass, genius, media_player)
        # hook media_player to sensor
        async_track_state_change(hass, media_player, genius_sensor.handle_state_change)
        # add new sensor to list
        sensors.append(genius_sensor)

    # add new sensors
    async_add_entities(sensors)

    # platform setup successfully
    return True


class GeniusLyricsSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, genius, media_entity_id):
        """Initialize the sensor"""
        self._genius = genius
        self._media_player_id = media_entity_id
        self._name = f'{split_entity_id(media_entity_id)[1]} Lyrics'
        self._state = STATE_OFF

        _LOGGER.debug(f"Creating sensor: {self.name}")

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        state_attrs = {
            ATTR_MEDIA_ARTIST: self._genius.artist,
            ATTR_MEDIA_TITLE: self._genius.title,
            ATTR_MEDIA_LYRICS: self._genius.lyrics,
            # TODO: add URL, Album Art
        }
        return state_attrs

    @property
    def should_poll(self) -> bool:
        return False

    def update(self):
        """Fetch new state data for the sensor"""
        self._genius.fetch_lyrics()

    def handle_state_change(self, entity_id, old_state, new_state):
        # ensure tracking entity_id
        if entity_id != self._media_player_id:
            return

        if new_state.state not in [STATE_PLAYING, STATE_PAUSED, STATE_BUFFERING]:
            self._genius.reset()
            self._state = STATE_OFF
            self.async_schedule_update_ha_state(True)
            return

        # must have music content type and something queued
        if new_state.attributes.get(ATTR_MEDIA_CONTENT_TYPE) != MEDIA_TYPE_MUSIC \
                and new_state.attributes.get(ATTR_MEDIA_DURATION):
            return

        # media title changed?
        if self._genius.title == new_state.attributes.get(ATTR_MEDIA_TITLE):
            return

        # all checks out..update artist and title to fetch
        self._genius.artist = new_state.attributes.get(ATTR_MEDIA_ARTIST)
        self._genius.title = new_state.attributes.get(ATTR_MEDIA_TITLE)
        self._state = STATE_ON

        # trigger update
        self.async_schedule_update_ha_state(True)


class GeniusLyrics:
    def __init__(self, access_token, genius=None):
        self.__artist = None
        self.__title = None
        self.__lyrics = None
        self.__genius = None

        from lyricsgenius import Genius
        # use or create Genius class
        if isinstance(genius, Genius):
            self.__genius = genius
        else:
            self.__genius = Genius(access_token, skip_non_songs=True)

    @property
    def artist(self):
        return self.__artist

    @artist.setter
    def artist(self, new_artist):
        self.__artist = new_artist
        _LOGGER.debug(f"Artist set to: {self.__artist}")

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, new_title):
        # filter out terms from title
        # TODO: move to CONFIG_SCHEMA
        exclude_terms = [
            '(explicit',
            '(feat',
        ]
        _new_title = str(new_title).lower()
        for term in exclude_terms:
            if term in _new_title:
                pos = _new_title.find(term)
                self.__title = new_title[0:pos].strip()
                break
        else:
            self.__title = new_title
        _LOGGER.debug(f"Title set to: {self.__title}")

    @property
    def lyrics(self):
        return self.__lyrics

    def fetch_lyrics(self, artist=None, title=None):
        if artist:
            self.__artist = artist
        if title:
            self.__title = title

        if self.__artist is None or self.__title is None:
            _LOGGER.debug("Missing artist and/or title")
            return

        _LOGGER.info(f"Search lyrics for artist='{self.__artist}' and title='{self.__title}'")

        song = self.__genius.search_song(self.__title, self.__artist, get_full_info=False)
        if song:
            _LOGGER.debug(f"Found song: artist = {song.artist}, title = {song.title}")

            # FIXME: need to avoid incorrectly found song lyrics
            # for now..comparing artist names suffices. Titles may differ (e.g. 'feat. John Doe')
            # if self.__title == song.title:
            #     _LOGGER.debug(f"Found lyrics: {song.lyrics}")

            # if str(self.__artist).lower() == str(song.artist).lower() \
            #         or str(song.title).lower() in str(self.__title).lower():

            self.__title = song.title
            self.__lyrics = song.lyrics
            return True
        else:
            self.__lyrics = "Lyrics not found"
            return False

    def reset(self):
        self.__artist = None
        self.__title = None
        self.__lyrics = None
