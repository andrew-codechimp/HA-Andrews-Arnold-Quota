"""Adds config flow for AndrewsArnoldQuota."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

from .const import DOMAIN

class AndrewsArnoldQuotaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AndrewsArnoldQuota."""

    VERSION = 1
    _reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user, unless one already exists."""
        errors = {}
        defaults = {
            CONF_USERNAME: "",
            CONF_PASSWORD: "",
        }

        if user_input is not None:
            if not self._reauth_entry:
                if self._async_current_entries():
                    return self.async_abort(reason="single_instance_allowed")
            return self.async_create_entry(title="Andrews & Arnold Quota", data=user_input)
        elif self._reauth_entry:
            for key in defaults:
                defaults[key] = self._reauth_entry.data.get(key)

        user_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME, default=defaults[CONF_USERNAME]): str,
                vol.Required(CONF_PASSWORD, default=defaults[CONF_PASSWORD]): str,
            },
        )

        return self.async_show_form(
            step_id="user", data_schema=user_schema, errors=errors
        )

    async def async_step_reauth(self, user_input: Mapping[str, Any]) -> FlowResult:
        """Perform reauth upon an API authentication error."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_user()
