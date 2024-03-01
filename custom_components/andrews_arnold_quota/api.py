"""Andrews & Arnold API Client."""

from __future__ import annotations
from logging import getLogger
from typing import Any

import aiohttp
from asyncio import timeout

from homeassistant.core import HomeAssistant

from .const import LOGGER


class AndrewsArnoldQuotaApiClient:
    """Andrews & Arnold API Client."""

    _url = "https://chaos2.aa.net.uk/broadband/"

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ) -> None:
        """Andrews & Arnold API Client."""
        self._session = session
        self._username = username
        self._password = password

        self._connected = False
        self._error = ""

    async def connection_test(self) -> tuple:
        """Test connection."""
        await self.query("quota")

        return self._connected, self._error

    async def query(
        self,
        service: str,
        params: dict[str, Any] | None = {},
    ) -> any:
        """Get information from the API."""

        error = False

        headers = {
            "Authorization": aiohttp.BasicAuth(self._username, self._password).encode(),
        }

        try:
            LOGGER.debug(
                "%s query: %s, %s",
                self._url,
                service,
                params,
            )

            async with timeout(10):
                response = await self._session.request(
                    method="get",
                    url=f"{self._url}{service}",
                    data=params,
                    headers=headers,
                )

                if response.status == 200:
                    data = await response.json()
                    LOGGER.debug(
                        "%s query response: %s",
                        self._url,
                        data,
                    )

                    if "error" in data:
                        error = True
                else:
                    error = True
        except Exception as exception:
            print(exception)
            error = True

        if error:
            try:
                if data and "error" in data:
                    errorcode = data["error"]
                else:
                    errorcode = response.status
            except Exception:
                errorcode = "no_response"

            LOGGER.warning(
                "%s unable to fetch data %s (%s)",
                self._url,
                service,
                errorcode,
            )

            self._error = errorcode
            return None

        self._connected = True
        self._error = ""

        return data

    @property
    def error(self):
        """Return error."""
        return self._error
