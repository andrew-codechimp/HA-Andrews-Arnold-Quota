"""Adds config flow for AndrewsArnoldQuota."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from aioandrewsarnold.andrewsarnold import AndrewsArnoldClient, AndrewsArnoldError, AndrewsArnoldAuthenticationError, InfoResponse

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from homeassistant.const import (
    CONF_PASSWORD,
    CONF_USERNAME,
)

from .const import DOMAIN, LOGGER

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

CONFIG_VERSION = 2


class AndrewsArnoldQuotaConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for AndrewsArnoldQuota."""

    VERSION = CONFIG_VERSION

    _reauth_entry: config_entries.ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user, unless one already exists."""

        errors = {}

        if not self._reauth_entry:
            if self._async_current_entries():
                return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            client = AndrewsArnoldClient(
                session=async_get_clientsession(self.hass),
                control_login=user_input[CONF_USERNAME],
                control_password=user_input[CONF_PASSWORD],
            )

            try:
                await client.get_info()

            except AndrewsArnoldAuthenticationError:
                return {"base": "invalid_auth"}, None
            except AndrewsArnoldError:
                return {"base": "unknown"}, None

            # Save instance
            if not errors:
                if self._reauth_entry is None:
                    await self.async_set_unique_id(user_input[CONF_USERNAME])
                    return self.async_create_entry(
                        title="Andrews & Arnold Quota", data=user_input
                    )
                else:
                    self.hass.config_entries.async_update_entry(
                        self._reauth_entry, data=user_input
                    )
                    await self.hass.config_entries.async_reload(
                        self._reauth_entry.entry_id
                    )
                    return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reauth(
        self, user_input=None  # pylint: disable=unused-argument
    ):
        """Perform reauth upon an API authentication error."""
        self._reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm",
                data_schema=vol.Schema({}),
            )
        self._reauth_config = True
        return await self.async_step_user()
