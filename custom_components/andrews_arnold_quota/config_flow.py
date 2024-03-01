"""Adds config flow for AndrewsArnoldQuota."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

from .api import AndrewsArnoldQuotaApiClient

from .const import DOMAIN, LOGGER


class AndrewsArnoldQuotaFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AndrewsArnoldQuota."""

    VERSION = 1
    _reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_import(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Occurs when a previous entry setup fails and is re-initiated."""
        return await self.async_step_user(user_input)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
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

            api = AndrewsArnoldQuotaApiClient(
                async_get_clientsession(self.hass),
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
            )

            conn, errorcode = await api.connection_test()

            if not conn:
                errors["base"] = errorcode
                LOGGER.error("Andrews & Arnold Quota connection error (%s)", errorcode)

            # Save instance
            if not errors:
                return self.async_create_entry(
                    title="Andrews & Arnold Quota", data=user_input
                )

            return self._show_config_form(user_input=user_input, errors=errors)

        return self._show_config_form(
            user_input={
                CONF_USERNAME: "",
                CONF_PASSWORD: "",
            },
            errors=errors,
        )

    async def async_step_reauth(self, user_input: Mapping[str, Any]) -> FlowResult:
        """Perform reauth upon an API authentication error."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_user()

    def _show_config_form(
        self, user_input: dict[str, Any] | None, errors: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show the configuration form."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=user_input[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=user_input[CONF_PASSWORD]): str,
                }
            ),
            errors=errors,
        )
