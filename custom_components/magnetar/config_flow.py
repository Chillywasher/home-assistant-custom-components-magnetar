"""Config flow for the Blustream SW42DA integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.device_registry import format_mac

from .api import MagnetarApi, POWER_ON
from .const import DOMAIN, CONF_BAUD_RATE


_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default="192.168.67.123"): cv.string,
        vol.Required(CONF_PORT, default=8102): cv.positive_int,
        vol.Required(CONF_BAUD_RATE, default=152000): cv.positive_int,
    }
)

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # TODO validate the data can be used to set up a connection.

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    api = MagnetarApi(data[CONF_HOST], data[CONF_PORT], data[CONF_BAUD_RATE])

    resp = await hass.async_add_executor_job(api.send_command, [POWER_ON])

    if not resp[0] == "ack\r\n":
        raise CannotConnect

    # Return info that you want to store in the config entry.
    return {
        "title": "Magnetar {0}".format(data[CONF_HOST]),
        CONF_HOST: data[CONF_HOST],
        CONF_PORT: data[CONF_PORT],
        CONF_BAUD_RATE: data[CONF_BAUD_RATE],
        "unique_id": data[CONF_HOST],
    }


class MagnetarConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Magnetar."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                _LOGGER.info(info)

                unique_id = format_mac(info["unique_id"])
                _LOGGER.info("Magnetar device found: %s", unique_id)

                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured(updates={
                    CONF_HOST: info[CONF_HOST],
                    CONF_PORT: info[CONF_PORT],
                    CONF_BAUD_RATE: info[CONF_BAUD_RATE]
                })

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
    pass

class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
    pass