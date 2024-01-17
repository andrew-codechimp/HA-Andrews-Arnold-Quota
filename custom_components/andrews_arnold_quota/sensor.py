"""Sensor platform for andrews_arnold_quota."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import (
    UnitOfInformation,
)

from .const import DOMAIN
from .coordinator import AndrewsArnoldQuotaDataUpdateCoordinator
from .entity import AndrewsArnoldQuotaEntity, AndrewsArnoldQuotaEntityDescription

@dataclass
class AndrewsArnoldQuotaSensorEntityDescription(
    AndrewsArnoldQuotaEntityDescription,
    SensorEntityDescription,
):
    """Class describing AndrewsArnoldQuota sensor entities."""


ENTITY_DESCRIPTIONS = (
    AndrewsArnoldQuotaSensorEntityDescription(
        key="monthly_quota_gb",
        translation_key="monthly_quota",
        entity_id="sensor.andrews_arnold_monthly_quota",
        icon="mdi:counter",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    AndrewsArnoldQuotaSensorEntityDescription(
        key="quota_remaining_gb",
        translation_key="quota_remaining",
        entity_id="sensor.andrews_arnold_quota_remaining",
        icon="mdi:counter",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
    ),
    AndrewsArnoldQuotaSensorEntityDescription(
        key="quota_status",
        translation_key="quota_status",
        entity_id="sensor.andrews_arnold_quota_status",
        icon="mdi:information-outline",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        AndrewsArnoldQuotaSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class AndrewsArnoldQuotaSensor(AndrewsArnoldQuotaEntity, SensorEntity):
    """andrews_arnold_quota Sensor class."""

    def __init__(
        self,
        coordinator: AndrewsArnoldQuotaDataUpdateCoordinator,
        entity_description: AndrewsArnoldQuotaSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(entity_description, coordinator)

        self.entity_description = entity_description
        self._attr_unique_id = (
            f"andrews_arnold_quota_{entity_description.key}".lower()
        )
        # self._attr_name = f"Andrews & Arnold Quota {entity_description.name}"
        self._attr_has_entity_name = True

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.entity_description.key, None)
