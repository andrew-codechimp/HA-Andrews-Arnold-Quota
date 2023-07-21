"""Sensor platform for andrews_arnold_quota."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from homeassistant.const import (
    DATA_GIGABYTES,
)

from .const import DOMAIN
from .coordinator import AndrewsArnoldQuotaDataUpdateCoordinator
from .entity import AndrewsArnoldQuotaEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="monthly_quota_gb",
        name="Monthly Quota",
        icon="mdi:counter",
        native_unit_of_measurement=DATA_GIGABYTES,
    ),
    SensorEntityDescription(
        key="quota_remaining_gb",
        name="Quota Remaining",
        icon="mdi:counter",
        native_unit_of_measurement=DATA_GIGABYTES,
    ),
    SensorEntityDescription(
        key="quota_status",
        name="Quota Status",
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
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_unique_id = f"andrews_arnold_{entity_description.key}".lower()
        self._attr_name = f'Andrews & Arnold Quota {entity_description.name}'
        self.entity_description = entity_description

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.entity_description.key, None)
