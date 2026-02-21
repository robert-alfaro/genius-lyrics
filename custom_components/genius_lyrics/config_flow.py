"""Config flow for Genius Lyrics integration."""

import logging
from typing import Any, Union

import voluptuous as vol

from homeassistant.components.media_player import DOMAIN as MP_DOMAIN
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_ENTITIES
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv

from .const import CONF_MONITOR_ALL, CONF_NOTIFY_NEW_PLAYERS, DOMAIN, INTEGRATION_NAME
from .helpers import get_media_player_entities

_LOGGER = logging.getLogger(__name__)


def _initial_form(flow: Union[ConfigFlow, OptionsFlow]):
    """Return flow form for init/user step id."""
    if isinstance(flow, ConfigFlow):
        step_id = "user"
        monitor_all = True
        notify_new_players = True
    elif isinstance(flow, OptionsFlow):
        step_id = "init"
        monitor_all = flow.config_entry.options.get(CONF_MONITOR_ALL, True)
        notify_new_players = flow.config_entry.options.get(
            CONF_NOTIFY_NEW_PLAYERS, True
        )
    else:
        raise TypeError("Invalid flow type")

    return flow.async_show_form(
        step_id=step_id,  # parameterized to follow guidance on using "user"
        data_schema=vol.Schema(
            {
                vol.Optional(CONF_MONITOR_ALL, default=monitor_all): cv.boolean,
                vol.Optional(
                    CONF_NOTIFY_NEW_PLAYERS, default=notify_new_players
                ): cv.boolean,
            }
        ),
        # TODO: would be nice to dynamically adjust per checkbox value on form
        last_step=False,
    )


def _select_entities_form(flow: Union[ConfigFlow, OptionsFlow]):
    """Return flow form for select_entities step id."""
    if isinstance(flow, ConfigFlow):
        monitored_entities = []
    elif isinstance(flow, OptionsFlow):
        monitored_entities = flow.config_entry.options.get(CONF_ENTITIES, [])
    else:
        raise TypeError("Invalid flow type")

    # get all available media_player entities
    available_entities = get_media_player_entities(flow.hass)

    return flow.async_show_form(
        step_id="select_entities",
        data_schema=vol.Schema(
            {
                vol.Required(
                    CONF_ENTITIES,
                    default=monitored_entities,
                ): cv.multi_select(available_entities),
            }
        ),
        last_step=True,
    )


class GeniusLyricsOptionsFlowHandler(OptionsFlow):
    """Handle Genius Lyrics options."""

    @property
    def config_entry(self):
        return self.hass.config_entries.async_get_entry(self.handler)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage Genius Lyrics options."""
        if user_input is not None:
            # user select to monitor all media players?
            if user_input[CONF_MONITOR_ALL] is True:
                _LOGGER.info("User selected to monitor ALL %s entities", MP_DOMAIN)
                return self.async_create_entry(title=INTEGRATION_NAME, data=user_input)

            # otherwise, proceed to the next step to select specific entities
            self._user_input = user_input
            return await self.async_step_select_entities()

        return _initial_form(self)

    async def async_step_select_entities(self, user_input=None):
        """Handle selecting specific entities."""

        if isinstance(user_input, dict) and user_input.get(CONF_ENTITIES):
            # combine the user input from both steps
            user_input.update(self._user_input)

            _LOGGER.info("User selected to monitor SPECIFIC %s entities", MP_DOMAIN)
            return self.async_create_entry(title=INTEGRATION_NAME, data=user_input)

        return _select_entities_form(self)


class GeniusLyricsFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Genius Lyrics config flow."""

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> GeniusLyricsOptionsFlowHandler:
        """Get the options flow for this handler."""
        return GeniusLyricsOptionsFlowHandler()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        # integration already configured?
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            # user select to monitor all media players?
            if user_input[CONF_MONITOR_ALL] is True:
                _LOGGER.info("User selected to monitor ALL %s entities", MP_DOMAIN)
                return self.async_create_entry(title=INTEGRATION_NAME, data=user_input)

            # otherwise, proceed to the next step to select specific entities
            self._user_input = user_input
            return await self.async_step_select_entities()

        return _initial_form(self)

    async def async_step_select_entities(self, user_input=None):
        """Handle selecting specific entities."""

        if isinstance(user_input, dict) and user_input.get(CONF_ENTITIES):
            # combine the user input from both steps
            user_input.update(self._user_input)

            _LOGGER.info("User selected to monitor SPECIFIC %s entities", MP_DOMAIN)
            return self.async_create_entry(title=INTEGRATION_NAME, data=user_input)

        return _select_entities_form(self)
