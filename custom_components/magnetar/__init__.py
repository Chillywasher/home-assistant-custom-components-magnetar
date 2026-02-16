"""The Magnetar integration."""

from __future__ import annotations

import logging

from homeassistant.helpers.typing import ConfigType
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, CONF_BAUD_RATE
from .api import MagnetarApi
from .coordinator import MagnetarCoordinator

_LOGGER = logging.getLogger(__name__)

_PLATFORMS: list[Platform] = [
    Platform.BUTTON,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Magnetar from a config entry."""

    controller = MagnetarApi(
        host=entry.data.get(CONF_HOST),
        port=entry.data.get(CONF_PORT),
        baud_rate=entry.data.get(CONF_BAUD_RATE)
    )

    magnetar_coordinator = MagnetarCoordinator(
        hass=hass,
        controller=controller,
        entry=entry,
    )

    await magnetar_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = magnetar_coordinator
    hass.data[DOMAIN]["controller"] = controller

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, _PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


