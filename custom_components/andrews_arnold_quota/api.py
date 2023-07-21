"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class AndrewsArnoldQuotaApiClientError(Exception):
    """Exception to indicate a general API error."""


class AndrewsArnoldQuotaApiClientCommunicationError(AndrewsArnoldQuotaApiClientError):
    """Exception to indicate a communication error."""


class AndrewsArnoldQuotaApiClientAuthenticationError(AndrewsArnoldQuotaApiClientError):
    """Exception to indicate an authentication error."""


class AndrewsArnoldQuotaApiClient:
    """Sample API Client."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._session = session

    async def async_get_data(self) -> any:
        """Get data from the API."""
        return await self._api_wrapper(method="get", url="https://quota.aa.net.uk")

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    allow_redirects=True,
                )
                if response.status in (401, 403):
                    raise AndrewsArnoldQuotaApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise AndrewsArnoldQuotaApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise AndrewsArnoldQuotaApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise AndrewsArnoldQuotaApiClientError(
                "Something really wrong happened!"
            ) from exception
