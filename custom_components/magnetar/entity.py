from __future__ import annotations

import logging

from datetime import datetime

from homeassistant.core import State
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MagnetarCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MagnetarEntity(CoordinatorEntity[MagnetarCoordinator], RestoreEntity):

    last_updated: datetime | None = None
    restored_state: State | None = None

    def send_command(self, command: list[str]):
        coordinator = self.coordinator
        coordinator.controller.send_command(command)

    @property
    def device_info(self) -> dict[str, object]:
        """Return the device_info of the device."""
        data = self.coordinator.data
        return {
            "identifiers": {(DOMAIN, "magnetar")},
            "name": "Magnetar",
            "manufacturer": "Magnetar",
            "model": "Unknown",
            "serial_number": "12345678",
        }
