"""Adds config flow for AndrewsArnoldQuota."""
from __future__ import annotations

from homeassistant import config_entries

from .const import DOMAIN

class AndrewsArnoldQuotaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AndrewsArnoldQuota."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Create entry, unless one already exists."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="Andrews & Arnold Quota", data={})
