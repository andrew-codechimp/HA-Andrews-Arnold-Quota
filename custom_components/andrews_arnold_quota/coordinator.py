"""DataUpdateCoordinator for andrews_arnold_quota."""

from __future__ import annotations

from datetime import timedelta

from aioandrewsarnold.andrewsarnold import AndrewsArnoldClient, AndrewsArnoldAuthenticationError, QuotaResponse

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN, LOGGER


class AndrewsArnoldQuotaDataUpdateCoordinator(DataUpdateCoordinator[QuotaResponse]):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    quotas: QuotaResponse

    def __init__(
        self,
        hass: HomeAssistant,
        client: AndrewsArnoldClient,
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
            self.quotas = await self.client.get_quotas()

        except AndrewsArnoldAuthenticationError as error:
            raise ConfigEntryAuthFailed("Unable to login, please re-login.") from error
        except Exception as error:
            raise UpdateFailed(error) from error

        return self.quotas
