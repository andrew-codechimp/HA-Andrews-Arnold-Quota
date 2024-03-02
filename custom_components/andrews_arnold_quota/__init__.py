"""Custom integration to integrate andrews_arnold_quota with Home Assistant.

For more details about this integration, please refer to
https://github.com/andrew-codechimp/HA-Andrews-Arnold-Quota
"""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import ConfigEntryAuthFailed

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

from .api import AndrewsArnoldQuotaApiClient
from .const import DOMAIN
from .coordinator import AndrewsArnoldQuotaDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})

    session = async_get_clientsession(hass)

    if CONF_USERNAME not in entry.data or CONF_PASSWORD not in entry.data:
        raise ConfigEntryAuthFailed("Unable to login, please re-login.") from None

    client = AndrewsArnoldQuotaApiClient(
        session=session,
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
    )

    conn, errorcode = await client.connection_test()

    if conn == False and errorcode == "Control authorisation failed":
        raise ConfigEntryAuthFailed("Unable to login, please re-login.") from None

    hass.data[DOMAIN][entry.entry_id] = coordinator = (
        AndrewsArnoldQuotaDataUpdateCoordinator(
            hass=hass,
            client=client,
        )
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
