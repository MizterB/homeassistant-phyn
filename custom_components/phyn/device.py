"""Phyn device object."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from aiophyn.api import API
from aiophyn.errors import RequestError
from async_timeout import timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.util.dt as dt_util

from .const import DOMAIN as PHYN_DOMAIN, LOGGER


class PhynDeviceDataUpdateCoordinator(DataUpdateCoordinator):
    """Phyn device object."""

    def __init__(
        self, hass: HomeAssistant, api_client: API, home_id: str, device_id: str
    ) -> None:
        """Initialize the device."""
        self.hass: HomeAssistant = hass
        self.api_client: API = api_client
        self._phyn_home_id: str = home_id
        self._phyn_device_id: str = device_id
        self._manufacturer: str = "Phyn"
        self._device_state: dict[str, Any] = {}
        self._water_usage: dict[str, Any] = {}
        super().__init__(
            hass,
            LOGGER,
            name=f"{PHYN_DOMAIN}-{device_id}",
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with timeout(20):
                await self._update_device()
                await self._update_consumption_data()
        except (RequestError) as error:
            raise UpdateFailed(error) from error

    @property
    def home_id(self) -> str:
        """Return Phyn home id."""
        return self._phyn_home_id

    @property
    def id(self) -> str:
        """Return Phyn device id."""
        return self._phyn_device_id

    @property
    def device_name(self) -> str:
        """Return device name."""
        return f"{self.manufacturer} {self.model}"

    @property
    def manufacturer(self) -> str:
        """Return manufacturer for device."""
        return self._manufacturer

    @property
    def model(self) -> str:
        """Return model for device."""
        return self._device_state["product_code"]

    @property
    def rssi(self) -> float:
        """Return rssi for device."""
        return self._device_state["signal_strength"]

    @property
    def available(self) -> bool:
        """Return True if device is available."""
        return self._device_state["online_status"]["v"] == "online"

    @property
    def current_flow_rate(self) -> float:
        """Return current flow rate in gpm."""
        return self._device_state["flow"]["mean"]

    @property
    def current_psi(self) -> float:
        """Return the current pressure in psi."""
        return self._device_state["pressure"]["mean"]

    @property
    def temperature(self) -> float:
        """Return the current temperature in degrees F."""
        return self._device_state["temperature"]["mean"]
        
    @property
    def current_psi1(self) -> float:
        """Return the current pressure in psi."""
        return self._device_state["pressure1"]["mean"]

    @property
    def temperature1(self) -> float:
        """Return the current temperature in degrees F."""
        return self._device_state["temperature1"]["mean"]
        
    @property
    def current_psi2(self) -> float:
        """Return the current pressure in psi."""
        return self._device_state["pressure2"]["mean"]

    @property
    def temperature2(self) -> float:
        """Return the current temperature in degrees F."""
        return self._device_state["temperature2"]["mean"]

    @property
    def consumption_today(self) -> float:
        """Return the current consumption for today in gallons."""
        return self._water_usage["water_consumption"]

    @property
    def firmware_version(self) -> str:
        """Return the firmware version for the device."""
        return self._device_state["fw_version"]

    @property
    def serial_number(self) -> str:
        """Return the serial number for the device."""
        return self._device_state["serial_number"]

    @property
    def valve_state(self) -> str:
        """Return the valve state for the device."""
        return self._device_state["sov_status"]["v"]

    async def _update_device(self, *_) -> None:
        """Update the device state from the API."""
        self._device_state = await self.api_client.device.get_state(
            self._phyn_device_id
        )
        LOGGER.debug("Phyn device state: %s", self._device_state)

    async def _update_consumption_data(self, *_) -> None:
        """Update water consumption data from the API."""
        today = dt_util.now().date()
        duration = today.strftime("%Y/%m/%d")
        self._water_usage = await self.api_client.device.get_consumption(
            self._phyn_device_id, duration
        )
        LOGGER.debug("Updated Phyn consumption data: %s", self._water_usage)
