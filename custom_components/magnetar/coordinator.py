import logging
from collections import defaultdict
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import COORDINATOR_NAME
from .api import MagnetarApi

_LOGGER = logging.getLogger(__name__)


class MagnetarCoordinator(DataUpdateCoordinator[defaultdict]):
    """Magnetar Coordinator"""

    def __init__(
            self,
            hass: HomeAssistant,
            entry: ConfigEntry,
            controller: MagnetarApi
    ) -> None:
        """Initialize the coordinator."""

        self.controller = controller
        self.hass = hass

        super().__init__(
            hass,
            _LOGGER,
            name=COORDINATOR_NAME,
            config_entry=entry,
            update_interval=timedelta(days=365)
        )

    async def _async_update_data(self) -> dict:
        return {}
