"""Platform for sensor integration."""
import logging
from typing import Any, Dict

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    PERCENTAGE,
    UnitOfTemperature,
)

from .const import DOMAIN, DEVICE_TYPE_MAP

_LOGGER = logging.getLogger(__name__)

# Define sensor types with icons
SENSOR_TYPES = {
    "temperature": {
        "device_class": SensorDeviceClass.TEMPERATURE,
        "unit_of_measurement": UnitOfTemperature.CELSIUS,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:thermometer",
    },
    "humidity": {
        "device_class": SensorDeviceClass.HUMIDITY,
        "unit_of_measurement": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:water-percent",
    },
    "power": {
        "device_class": SensorDeviceClass.BATTERY,
        "unit_of_measurement": PERCENTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:battery",
    },
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = []
    # Create sensors for each device and each available metric
    if coordinator.data:
        for mac, device_data in coordinator.data.items():
            for sensor_type in SENSOR_TYPES:
                if sensor_type in device_data:
                    entities.append(JaaleeSensor(coordinator, mac, sensor_type))
    
    async_add_entities(entities)


class JaaleeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Jaalee Sensor."""

    def __init__(self, coordinator, mac: str, sensor_type: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._mac = mac
        self._sensor_type = sensor_type
        
        # Initial data
        self._update_internal_state()

    def _update_internal_state(self):
        """Update properties of the entity based on coordinator data."""
        device_data = self.coordinator.data.get(self._mac, {})
        
        self._attr_name = f"{device_data.get('alias', self._mac)} {self._sensor_type.capitalize()}"
        self._attr_unique_id = f"{self._mac}_{self._sensor_type}"
        
        sensor_details = SENSOR_TYPES[self._sensor_type]
        self._attr_device_class = sensor_details.get("device_class")
        self._attr_native_unit_of_measurement = sensor_details.get("unit_of_measurement")
        self._attr_state_class = sensor_details.get("state_class")
        self._attr_icon = sensor_details.get("icon")
        
        value = device_data.get(self._sensor_type)
        
        # Round the values as requested
        if value is not None:
            try:
                if self._sensor_type == "temperature":
                    value = round(float(value), 1)
                elif self._sensor_type == "humidity":
                    value = round(float(value))
            except (ValueError, TypeError):
                _LOGGER.warning("Could not parse value for %s: %s", self.entity_id, value)
                value = None

        self._attr_native_value = value

    @property
    def device_info(self) -> Dict[str, Any]:
        """Return device information."""
        device_data = self.coordinator.data.get(self._mac, {})
        return {
            "identifiers": {(DOMAIN, self._mac)},
            "name": device_data.get("alias", self._mac),
            "manufacturer": "Jaalee",
            "model": DEVICE_TYPE_MAP.get(device_data.get("type"), device_data.get("type")),
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_internal_state()
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self._mac in self.coordinator.data
