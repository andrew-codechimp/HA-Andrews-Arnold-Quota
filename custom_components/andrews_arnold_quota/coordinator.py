"""DataUpdateCoordinator for andrews_arnold_quota."""
# mypy: disable-error-code="no-untyped-def,method-assign,misc"

from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    UpdateFailed,
    DataUpdateCoordinator,
)

from .api import AndrewsArnoldQuotaApiClient
from .const import DOMAIN, LOGGER

RETRY_TIMES = 4


class AndrewsArnoldQuotaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    quota = any
    retry_count = 0

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
        """Update data."""

        try:
            data = await self.client.query("quota")
            if self.client.error in {
                "Control authorisation failed",
                "Bad control-login",
            }:
                raise ConfigEntryAuthFailed(
                    "Unable to login, please re-login."
                ) from None

            self.quota = data
            self.retry_count = 0

        except Exception as exception:
            self.retry_count += 1

            if self.retry_count >= RETRY_TIMES:
                self.retry_count = 0
                raise UpdateFailed(exception) from exception

        return self.quota
