"""Support for Phyn Water Monitor sensors."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN as PHYN_DOMAIN
from .device import PhynDeviceDataUpdateCoordinator
from .entity import PhynEntity

WATER_ICON = "mdi:water"
GAUGE_ICON = "mdi:gauge"
NAME_DAILY_USAGE = "Daily water usage"
NAME_FLOW_RATE = "Average water flow rate"
NAME_WATER_TEMPERATURE = "Average water temperature"
NAME_HOT_WATER_TEMPERATURE = "Average hot water temperature"
NAME_COLD_WATER_TEMPERATURE = "Average cold water temperature"
NAME_WATER_PRESSURE = "Average water pressure"
NAME_HOT_WATER_PRESSURE = "Average hot water pressure"
NAME_COLD_WATER_PRESSURE = "Average cold water pressure"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flo sensors from config entry."""
    devices: list[PhynDeviceDataUpdateCoordinator] = hass.data[PHYN_DOMAIN][
        config_entry.entry_id
    ]["devices"]
    entities = []
    for device in devices:
        if device.model == 'PC1':
            entities.extend([
                PhynDailyUsageSensor(device),
                PhynTemperature1Sensor(NAME_HOT_WATER_TEMPERATURE, device),
                PhynPressure1Sensor(NAME_HOT_WATER_PRESSURE, device),
                PhynTemperature2Sensor(NAME_COLD_WATER_TEMPERATURE, device),
                PhynPressure2Sensor(NAME_COLD_WATER_PRESSURE, device),
            ])
        else:
            entities.extend([
                PhynDailyUsageSensor(device),
                PhynCurrentFlowRateSensor(device),
                PhynTemperatureSensor(NAME_WATER_TEMPERATURE, device),
                PhynPressureSensor(device),
            ])
    async_add_entities(entities)


class PhynDailyUsageSensor(PhynEntity, SensorEntity):
    """Monitors the daily water usage."""

    _attr_icon = WATER_ICON
    _attr_native_unit_of_measurement = UnitOfVolume.GALLONS
    _attr_state_class: SensorStateClass = SensorStateClass.TOTAL_INCREASING
    _attr_device_class = SensorDeviceClass.WATER

    def __init__(self, device):
        """Initialize the daily water usage sensor."""
        super().__init__("daily_consumption", NAME_DAILY_USAGE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current daily usage."""
        if self._device.consumption_today is None:
            return None
        return round(self._device.consumption_today, 1)


class PhynCurrentFlowRateSensor(PhynEntity, SensorEntity):
    """Monitors the current water flow rate."""

    _attr_device_class = SensorDeviceClass.WATER
    _attr_native_unit_of_measurement = UnitOfVolume.GALLONS
    _attr_state_class: SensorStateClass = SensorStateClass.TOTAL

    def __init__(self, device):
        """Initialize the flow rate sensor."""
        super().__init__("current_flow_rate", NAME_FLOW_RATE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current flow rate."""
        if self._device.current_flow_rate is None:
            return None
        return round(self._device.current_flow_rate, 1)


class PhynTemperatureSensor(PhynEntity, SensorEntity):
    """Monitors the temperature."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, name, device):
        """Initialize the temperature sensor."""
        super().__init__("temperature", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current temperature."""
        if self._device.temperature is None:
            return None
        return round(self._device.temperature, 1)


class PhynPressureSensor(PhynEntity, SensorEntity):
    """Monitors the water pressure."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = UnitOfPressure.PSI
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        """Initialize the pressure sensor."""
        super().__init__("water_pressure", NAME_WATER_PRESSURE, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current water pressure."""
        if self._device.current_psi is None:
            return None
        return round(self._device.current_psi, 1)
        
class PhynTemperature1Sensor(PhynEntity, SensorEntity):
    """Monitors the temperature1."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, name, device):
        """Initialize the temperature 1 sensor."""
        super().__init__("temperature1", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current temperature 1."""
        if self._device.temperature1 is None:
            return None
        return round(self._device.temperature1, 1)


class PhynPressure1Sensor(PhynEntity, SensorEntity):
    """Monitors the water pressure1."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = UnitOfPressure.PSI
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, name, device):
        """Initialize the pressure1 sensor."""
        super().__init__("water_pressure1", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current water pressure1."""
        if self._device.current_psi1 is None:
            return None
        return round(self._device.current_psi1, 1)
        
class PhynTemperature2Sensor(PhynEntity, SensorEntity):
    """Monitors the temperature2."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = UnitOfTemperature.FAHRENHEIT
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, name, device):
        """Initialize the temperature2 sensor."""
        super().__init__("temperature2", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current temperature2."""
        if self._device.temperature2 is None:
            return None
        return round(self._device.temperature2, 1)


class PhynPressure2Sensor(PhynEntity, SensorEntity):
    """Monitors the water pressure2."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_native_unit_of_measurement = UnitOfPressure.PSI
    _attr_state_class: SensorStateClass = SensorStateClass.MEASUREMENT

    def __init__(self, name, device):
        """Initialize the pressure2 sensor."""
        super().__init__("water_pressure2", name, device)
        self._state: float = None

    @property
    def native_value(self) -> float | None:
        """Return the current water pressure2."""
        if self._device.current_psi2 is None:
            return None
        return round(self._device.current_psi2, 1)
