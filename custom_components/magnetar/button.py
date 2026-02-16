"""Platform for sensor integration."""
import asyncio
import logging

from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.button import (
    ButtonEntity, ButtonEntityDescription,
)
from homeassistant.core import HomeAssistant, State

from .api import (SUBS_ENGLISH, STOP, PLAY, PAUSE, POWER_ON, POWER_OFF, MUTE,
                  NAVIGATE_UP, NAVIGATE_DOWN, NAVIGATE_LEFT, NAVIGATE_RIGHT, FAST_FORWARD, REWIND, NEXT_TRACK,
                  PREVIOUS_TRACK, NAVIGATE_CONFIRM)
from .const import DOMAIN
from .coordinator import MagnetarCoordinator
from .entity import MagnetarEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class MagnetarButtonDescription(ButtonEntityDescription):
    press_command: list[str] | None = None

BUTTONS: tuple[MagnetarButtonDescription, ...] = (
    MagnetarButtonDescription(
        key="subtitles",
        name="Subtitles",
        press_command=SUBS_ENGLISH,
    ),
    MagnetarButtonDescription(
        key="stop",
        name="Stop",
        press_command=[STOP],
    ),
    MagnetarButtonDescription(
        key="play",
        name="Play",
        press_command=[PLAY],
    ),
    MagnetarButtonDescription(
        key="pause",
        name="Pause",
        press_command=[PAUSE],
    ),
    MagnetarButtonDescription(
        key="power_on",
        name="Power On",
        press_command=[POWER_ON],
    ),
    MagnetarButtonDescription(
        key="power_off",
        name="Power Off",
        press_command=[POWER_OFF],
    ),
    MagnetarButtonDescription(
        key="mute",
        name="Mute",
        press_command=[MUTE],
    ),
    MagnetarButtonDescription(
        key="navigate_confirm",
        name="Navigate Confirm",
        press_command=[NAVIGATE_CONFIRM],
    ),
    MagnetarButtonDescription(
        key="navigate_up",
        name="Navigate Up",
        press_command=[NAVIGATE_UP],
    ),
    MagnetarButtonDescription(
        key="navigate_down",
        name="Navigate Down",
        press_command=[NAVIGATE_DOWN],
    ),
    MagnetarButtonDescription(
        key="navigate_left",
        name="Navigate Left",
        press_command=[NAVIGATE_LEFT],
    ),
    MagnetarButtonDescription(
        key="navigate_right",
        name="Navigate Right",
        press_command=[NAVIGATE_RIGHT],
    ),
    MagnetarButtonDescription(
        key="fast_forward",
        name="Fast Forward",
        press_command=[FAST_FORWARD],
    ),
    MagnetarButtonDescription(
        key="rewind",
        name="Rewind",
        press_command=[REWIND],
    ),
    MagnetarButtonDescription(
        key="next_track",
        name="Next Track",
        press_command=[NEXT_TRACK],
    ),
    MagnetarButtonDescription(
        key="previous_track",
        name="Previous Track",
        press_command=[PREVIOUS_TRACK],
    ),
)


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    """Set up the Magnetar button entity."""
    coordinator: MagnetarCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        MagnetarButton(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in BUTTONS
    )


class MagnetarButton(MagnetarEntity, ButtonEntity):
    """ Representation of an Sw42da button """

    entity_description: MagnetarButtonDescription
    _attr_has_entity_name = True

    last_updated: datetime | None = None
    restored_state: State | None = None

    def __init__(
            self,
            coordinator: MagnetarCoordinator,
            entity_description: MagnetarButtonDescription,

    ) -> None:
        super().__init__(coordinator=coordinator)
        self.entity_description = entity_description
        self.entity_id = f"button.{DOMAIN}_{entity_description.key}"
        self._attr_unique_id = f"{DOMAIN}_button_{entity_description.key}"
        self._attr_name = entity_description.name

    async def async_press(self, **kwargs: object) -> None:
        """Press button."""
        try:
            _LOGGER.debug("Pressing button %s", self._attr_name)
            await self.hass.async_add_executor_job(
                self.send_command, self.entity_description.press_command
            )
            await asyncio.sleep(1)
            await self.coordinator.async_refresh()
        except Exception as err:
            _LOGGER.error("Failed to press %s: %s", self._attr_name, err)
            raise
