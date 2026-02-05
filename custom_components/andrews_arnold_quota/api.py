"""Andrews & Arnold API Client."""
# mypy: disable-error-code="no-untyped-def"

from __future__ import annotations

from typing import Any
from asyncio import timeout

import aiohttp

from .const import LOGGER, API_URL


class AndrewsArnoldQuotaApiClient:
    """Andrews & Arnold API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        username: str,
        password: str,
    ) -> None:
        """Andrews & Arnold API Client."""
        self._url = API_URL
        self._session = session
        self._username = username
        self._password = password

        self._connected = False
        self._error = ""

    async def connection_test(self) -> tuple:
        """Test connection."""
        await self.query("quota")

        return self._connected, self._error

    async def query(self, service: str, params: dict[str, Any] | None = None) -> Any:
        """Get information from the API."""

        if params is None:
            params = {}

        error = False

        params["control_login"] = self._username
        params["control_password"] = self._password

        try:
            async with timeout(10):
                response = await self._session.request(
                    method="post",
                    url=f"{self._url}{service}",
                    data=params,
                )

                if response.status == 200:
                    data = await response.json()
                    LOGGER.debug(
                        "%s query response: %s",
                        f"{self._url}{service}",
                        data,
                    )

                    if "error" in data:
                        error = True
                else:
                    error = True
        except Exception:  # noqa: BLE001
            error = True

        if error:
            try:
                if data and "error" in data:
                    errorcode = data["error"]
                else:
                    errorcode = response.status
            except Exception:  # noqa: BLE001
                errorcode = "no_connection"

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
