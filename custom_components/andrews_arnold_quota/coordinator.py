"""DataUpdateCoordinator for andrews_arnold_quota."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import AndrewsArnoldQuotaApiClient
from .const import DOMAIN, LOGGER


class AndrewsArnoldQuotaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    quota = any

    def __init__(
        self,
        hass: HomeAssistant,
        client: AndrewsArnoldQuotaApiClient,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            self.quota = await self.client.query("quota")
        except Exception as exception:
            if self.client.error == "Account authorisation failed":
                raise ConfigEntryAuthFailed(
                    "Unable to login, please re-login."
                ) from None

            raise UpdateFailed(exception) from exception

        return self.quota
