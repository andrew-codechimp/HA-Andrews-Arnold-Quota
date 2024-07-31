"""Sensor platform for andrews_arnold_quota."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from aioandrewsarnold import Info

from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import (
    UnitOfInformation,
)
from homeassistant.helpers.typing import StateType
from homeassistant.helpers import entity_registry as er

from .coordinator import AndrewsArnoldInfoCoordinator, AndrewsArnoldConfigEntry

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import ATTRIBUTION, DOMAIN, NAME, MANUFACTURER


@dataclass(kw_only=True)
class AndrewsArnoldInfoSensorEntityDescription(SensorEntityDescription):
    """Class describing AndrewsArnoldQuota sensor entities."""

    entity_id: str | None = None
    value_fn: Callable[[Info], StateType]


ENTITY_DESCRIPTIONS = (
    AndrewsArnoldInfoSensorEntityDescription(
        key="monthly_quota_gb",
        translation_key="monthly_quota",
        entity_id="sensor.andrews_arnold_{service_id}_monthly_quota",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        value_fn=lambda quota: quota.quota_monthly,
    ),
    AndrewsArnoldInfoSensorEntityDescription(
        key="quota_remaining_gb",
        translation_key="quota_remaining",
        entity_id="sensor.andrews_arnold__{service_id}_quota_remaining",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        value_fn=lambda quota: quota.quota_remaining,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AndrewsArnoldConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the sensor platform."""
    coordinator = entry.runtime_data.coordinator

    added_services: list[Info] = []

    assert entry.unique_id is not None

    def _async_delete_entities(services: list[Info]) -> None:
        """Delete entities for removed services."""
        entity_registry = er.async_get(hass)
        for service_id in services:
            entity_id = entity_registry.async_get_entity_id(
                SENSOR_DOMAIN, DOMAIN, f"{entry.unique_id}_{service_id}"
            )
            if entity_id:
                entity_registry.async_remove(entity_id)

    def _async_entity_listener() -> None:
        """Handle additions/deletions of shopping lists."""
        received_services = coordinator.data.services

        new_services = [
            i for n, i in enumerate(received_services) if i not in added_services[:n]
        ]
        removed_services = [
            i for n, i in enumerate(added_services) if i not in received_services[:n]
        ]

        if new_services:
            for service in new_services:
                async_add_entities(
                    AndrewsArnoldSensor(coordinator, entity_description, service)
                    for entity_description in ENTITY_DESCRIPTIONS
                )
        if removed_services:
            _async_delete_entities(removed_services)

    coordinator.async_add_listener(_async_entity_listener)
    _async_entity_listener()


class AndrewsArnoldSensor(
    CoordinatorEntity[AndrewsArnoldInfoCoordinator], SensorEntity
):
    """andrews_arnold_quota Sensor class."""

    coordinator: AndrewsArnoldInfoCoordinator
    entity_description: AndrewsArnoldInfoSensorEntityDescription
    service_id: str

    def __init__(
        self,
        coordinator: AndrewsArnoldInfoCoordinator,
        entity_description: AndrewsArnoldInfoSensorEntityDescription,
        service: Info,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)

        self.service_id = service.service_id
        entity_description.entity_id = entity_description.entity_id.replace(
            "{service_id}", service.service_id
        )

        self._attr_translation_key = entity_description.translation_key
        self._attr_translation_placeholders = {"service_id": service.service_id}

        self._attr_unique_id = f"andrews_arnold_quota_{service.service_id}_{entity_description.key}".lower()
        self._attr_has_entity_name = True

        self.coordinator = coordinator
        self.entity_description = entity_description

        self._attr_attribution = ATTRIBUTION

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.service_id)},
            name=NAME,
            manufacturer=MANUFACTURER,
            model=f"{service.postcode} - {service.login}",
        )

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""

        for service in self.coordinator.data.services:
            if service.service_id == self.service_id:
                return round(
                    int(self.entity_description.value_fn(service)) / 1000000000,
                    1,
                )
        return None
