"""Switch representing the shutoff valve for the Phyn integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as PHYN_DOMAIN
from .device import PhynDeviceDataUpdateCoordinator
from .entity import PhynEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Phyn switches from config entry."""
    devices: list[PhynDeviceDataUpdateCoordinator] = hass.data[PHYN_DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        entities.extend(
            [
                PhynValveSwitch(device),
                PhynAwayModeSwitch(device)
            ]
        )
    async_add_entities(entities)


class PhynValveSwitch(PhynEntity, SwitchEntity):
    """Switch class for the Phyn valve."""

    def __init__(self, device: PhynDeviceDataUpdateCoordinator) -> None:
        """Initialize the Phyn valve switch."""
        super().__init__("shutoff_valve", "Shutoff valve", device)
        self._state = self._device.valve_state == "Open"

    @property
    def is_on(self) -> bool:
        """Return True if the valve is open."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the valve."""
        if self.is_on:
            return "mdi:valve-open"
        return "mdi:valve-closed"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Open the valve."""
        await self._device.api_client.device.open_valve(self._device.id)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Close the valve."""
        await self._device.api_client.device.close_valve(self._device.id)
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest valve state and update the state machine."""
        self._state = self._device.valve_state == "Open"
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))

class PhynAwayModeSwitch(PhynEntity, SwitchEntity):
    """Switch class for the Phyn Away Mode."""

    def __init__(self, device: PhynDeviceDataUpdateCoordinator) -> None:
        """Initialize the Phyn Away Mode switch."""
        super().__init__("away_mode", "Away Mode", device)
        self._state = self._device.away_mode

    @property
    def is_on(self) -> bool:
        """Return True if away mode is on."""
        return self._state

    @property
    def icon(self):
        """Return the icon to use for the away mode."""
        if self.is_on:
            return "mdi:bag-suitcase"
        return "mdi:home-circle"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Open the valve."""
        await self._device.api_client.device.enable_away_mode(self._device.id)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Close the valve."""
        await self._device.api_client.device.disable_away_mode(self._device.id)
        self._state = False
        self.async_write_ha_state()

    @callback
    def async_update_state(self) -> None:
        """Retrieve the latest valve state and update the state machine."""
        self._state = self._device.away_mode
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(self._device.async_add_listener(self.async_update_state))