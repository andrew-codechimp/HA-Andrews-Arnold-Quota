"""DataUpdateCoordinator for andrews_arnold_quota."""

from __future__ import annotations

from datetime import timedelta
from dataclasses import dataclass

from aioandrewsarnold.andrewsarnold import AndrewsArnoldClient, AndrewsArnoldAuthenticationError, InfoResponse

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .const import DOMAIN, LOGGER

@dataclass
class AndrewsArnoldData:
    """Andrews & Arnold data type."""

    client: AndrewsArnoldClient
    coordinator: AndrewsArnoldInfoCoordinator


type AndrewsArnoldConfigEntry = ConfigEntry[AndrewsArnoldData]


class AndrewsArnoldInfoCoordinator(DataUpdateCoordinator[InfoResponse]):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry
    info: InfoResponse

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
            self.info = await self.client.get_info()

        except AndrewsArnoldAuthenticationError as error:
            raise ConfigEntryAuthFailed("Unable to login, please re-login.") from error
        except Exception as error:
            raise UpdateFailed(error) from error

        return self.info
