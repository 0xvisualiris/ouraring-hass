'''Support for Oura Ring sensors.'''
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from .const import DOMAIN

@dataclass
class OuraRingSensorEntityDescription(SensorEntityDescription):
    '''Class describing Oura Ring sensor entities.'''
    value_fn: Callable[[dict[str, Any]], StateType] | None = None

SENSORS: tuple[OuraRingSensorEntityDescription, ...] = (
    OuraRingSensorEntityDescription(
        key="sleep_score",
        name="Sleep Score",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("sleep_score"),
        icon="mdi:sleep",
    ),
    OuraRingSensorEntityDescription(
        key="readiness_score",
        name="Readiness Score",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("readiness_score"),
        icon="mdi:heart-pulse",
    ),
    OuraRingSensorEntityDescription(
        key="activity_score",
        name="Activity Score",
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("activity_score"),
        icon="mdi:run",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    '''Set up the Oura Ring sensors.'''
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        OuraRingSensor(coordinator, description, entry)
        for description in SENSORS
    )

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
