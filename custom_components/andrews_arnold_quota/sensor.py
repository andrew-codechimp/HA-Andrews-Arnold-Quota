"""Sensor platform for andrews_arnold_quota."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import (
    UnitOfInformation,
)
from homeassistant.util import slugify

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
        entity_id="sensor.andrews_arnold_{line_id}_monthly_quota",
        icon="mdi:counter",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        api_field="quota_monthly",
    ),
    AndrewsArnoldQuotaSensorEntityDescription(
        key="quota_remaining_gb",
        translation_key="quota_remaining",
        entity_id="sensor.andrews_arnold_{line_id}_quota_remaining",
        icon="mdi:counter",
        native_unit_of_measurement=UnitOfInformation.GIGABYTES,
        api_field="quota_remaining",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    if coordinator.data:
        for line in coordinator.data["quota"]:
            {
                async_add_devices(
                    AndrewsArnoldQuotaSensor(
                        coordinator=coordinator,
                        entity_description=entity_description,
                        line_id = line["ID"]
                    )
                    for entity_description in ENTITY_DESCRIPTIONS
                )
            }

class AndrewsArnoldQuotaSensor(AndrewsArnoldQuotaEntity, SensorEntity):
    """andrews_arnold_quota Sensor class."""

    def __init__(
        self,
        coordinator: AndrewsArnoldQuotaDataUpdateCoordinator,
        entity_description: AndrewsArnoldQuotaSensorEntityDescription,
        line_id: str,
    ) -> None:
        """Initialize the sensor class."""

        entity_description.entity_id = entity_description.entity_id.replace("{line_id}", slugify(line_id.lower()))
        self._attr_translation_placeholders = {"line_id": line_id}

        super().__init__(entity_description, coordinator)

        self.entity_description = entity_description
        self._attr_unique_id = f"andrews_arnold_quota_{line_id}_{entity_description.key}".lower()
        self._attr_has_entity_name = True

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        if (
            self.coordinator.data
            and "quota" in self.coordinator.data
            and self.entity_description.api_field in self.coordinator.data["quota"][0]
        ):
            return round(
                int(
                    self.coordinator.data["quota"][0][self.entity_description.api_field]
                )
                / 1000000000,
                1,
            )
        return None
