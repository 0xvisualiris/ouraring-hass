'''Support for Oura Ring sensors.'''
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from .const import DOMAIN, CONF_SENSORS, SENSOR_OPTIONS

@dataclass
class OuraRingSensorEntityDescription(SensorEntityDescription):
    '''Class describing Oura Ring sensor entities.'''
    value_fn: Callable[[dict[str, Any]], StateType] | None = None

SENSORS: dict[str, OuraRingSensorEntityDescription] = {
    "sleep_score": OuraRingSensorEntityDescription(
        key="sleep_score",
        name="Sleep Score",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("sleep_score"),
        icon="mdi:sleep",
    ),
    "readiness_score": OuraRingSensorEntityDescription(
        key="readiness_score",
        name="Readiness Score",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("readiness_score"),
        icon="mdi:heart-pulse",
    ),
    "activity_score": OuraRingSensorEntityDescription(
        key="activity_score",
        name="Activity Score",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("activity_score"),
        icon="mdi:run",
    ),
    "cardiovascular_age": OuraRingSensorEntityDescription(
        key="cardiovascular_age",
        name="Cardiovascular Age",
        value_fn=lambda data: data.get("cardiovascular_age"),
        icon="mdi:heart-cog",
    ),
    "resilience": OuraRingSensorEntityDescription(
        key="resilience",
        name="Resilience",
        value_fn=lambda data: data.get("resilience"),
        icon="mdi:shield-heart",
    ),
    "spo2": OuraRingSensorEntityDescription(
        key="spo2",
        name="SpO2",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("spo2"),
        icon="mdi:oxygen",
    ),
    "stress": OuraRingSensorEntityDescription(
        key="stress",
        name="Stress Level",
        value_fn=lambda data: data.get("stress"),
        icon="mdi:emoticon-sad",
    ),
    "heartrate": OuraRingSensorEntityDescription(
        key="heartrate",
        name="Heart Rate",
        value_fn=lambda data: data.get("heartrate"),
        icon="mdi:heart-pulse",
    ),
    "rest_mode": OuraRingSensorEntityDescription(
        key="rest_mode",
        name="Rest Mode",
        value_fn=lambda data: data.get("rest_mode"),
        icon="mdi:bed",
    ),
}

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    '''Set up Oura Ring sensors based on user selection.'''
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    
    # Get selected sensors from config entry
    selected_sensors = entry.data.get(CONF_SENSORS, [])

    # Filter the sensors based on the selection
    sensors_to_add = [
        OuraRingSensor(coordinator, SENSORS[sensor], entry)
        for sensor in selected_sensors if sensor in SENSORS
    ]

    async_add_entities(sensors_to_add, True)

class OuraRingSensor(CoordinatorEntity[DataUpdateCoordinator], SensorEntity):
    '''Implementation of an Oura Ring sensor.'''

    entity_description: OuraRingSensorEntityDescription

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: OuraRingSensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        '''Initialize the sensor.'''
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_has_entity_name = True

    @property
    def native_value(self) -> StateType:
        '''Return the value reported by the sensor.'''
        if not self.coordinator.data:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
