"""Adds config flow for AndrewsArnoldQuota."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    AndrewsArnoldQuotaApiClient,
    AndrewsArnoldQuotaApiClientAuthenticationError,
    AndrewsArnoldQuotaApiClientCommunicationError,
    AndrewsArnoldQuotaApiClientError,
)
from .const import DOMAIN, LOGGER


class AndrewsArnoldQuotaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AndrewsArnoldQuota."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="Andrews & Arnold Quota", data={})
