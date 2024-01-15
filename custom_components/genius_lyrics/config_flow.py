"""Config flow for Genius Lyrics."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_ENTITIES
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv, entity_registry as er
from homeassistant.components.media_player import DOMAIN as MP_DOMAIN

from .const import CONF_MONITOR_ALL, DOMAIN, INTEGRATION_NAME

_LOGGER = logging.getLogger(__name__)


class GeniusLyricsOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Genius Lyrics options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize Genius Lyrics options flow."""
        self.config_entry = config_entry

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

        # get stored options
        monitor_all = self.config_entry.options.get(CONF_MONITOR_ALL, True)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_MONITOR_ALL, default=monitor_all): cv.boolean,
                }
            ),
        )

    async def async_step_select_entities(self, user_input=None):
        """Handle selecting specific entities."""

        if isinstance(user_input, dict) and user_input.get(CONF_ENTITIES):
            # combine the user input from both steps
            user_input.update(self._user_input)

            _LOGGER.info("User selected to monitor SPECIFIC %s entities", MP_DOMAIN)
            return self.async_create_entry(title=INTEGRATION_NAME, data=user_input)

        # get stored options
        monitored_entities = self.config_entry.options.get(CONF_ENTITIES, [])

        # get all available media_player entities
        available_entities = self.hass.states.async_entity_ids(MP_DOMAIN)

        return self.async_show_form(
            step_id="select_entities",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ENTITIES,
                        default=monitored_entities,
                    ): cv.multi_select(available_entities),
                }
            ),
        )


class GeniusLyricsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a Genius Lyrics config flow."""

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> GeniusLyricsOptionsFlowHandler:
        """Get the options flow for this handler."""
        return GeniusLyricsOptionsFlowHandler(config_entry)

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

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_MONITOR_ALL, default=True): cv.boolean,
                }
            ),
        )

    async def async_step_select_entities(self, user_input=None):
        """Handle selecting specific entities."""

        if isinstance(user_input, dict) and user_input.get(CONF_ENTITIES):
            # combine the user input from both steps
            user_input.update(self._user_input)

            _LOGGER.info("User selected to monitor SPECIFIC %s entities", MP_DOMAIN)
            return self.async_create_entry(title=INTEGRATION_NAME, data=user_input)

        # get all available media_player entities
        available_entities = self.hass.states.async_entity_ids(MP_DOMAIN)

        return self.async_show_form(
            step_id="select_entities",
            data_schema=vol.Schema(
                {
                    CONF_ENTITIES: cv.multi_select(available_entities),
                }
            ),
        )
