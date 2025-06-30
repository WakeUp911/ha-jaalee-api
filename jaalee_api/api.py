"""API client for Jaalee sensors."""
import asyncio
import logging
from typing import Any, Dict

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    API_TIMEOUT,
    GET_CODE_URL,
    LOGIN_URL,
    GET_ALL_DATA_URL,
)

_LOGGER = logging.getLogger(__name__)

class JaaleeApiClient:
    """Class to communicate with the Jaalee API."""

    def __init__(
        self,
        hass: HomeAssistant,
        email: str,
        token: str | None = None,
    ) -> None:
        """Initialize the API client."""
        self._hass = hass
        self._session = async_get_clientsession(hass)
        self.email = email
        self.token = token
        self.timezone = str(hass.config.time_zone)

    async def async_get_code(self) -> bool:
        """Request a verification code."""
        params = {"account": self.email}
        try:
            async with self._session.get(
                GET_CODE_URL, params=params, timeout=API_TIMEOUT
            ) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Get code response: %s", data)
                return data.get("code") == 0
        except aiohttp.ClientError as err:
            _LOGGER.error("Error requesting verification code: %s", err)
            return False

    async def async_login(self, code: str) -> str | None:
        """Log in and retrieve the authentication token."""
        payload = {
            "account": self.email,
            "code": code,
            "timeZone": self.timezone,
        }
        try:
            async with self._session.post(
                LOGIN_URL, json=payload, timeout=API_TIMEOUT
            ) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Login response: %s", data)
                if data.get("code") == 0 and data.get("data", {}).get("token"):
                    self.token = data["data"]["token"]
                    return self.token
                return None
        except aiohttp.ClientError as err:
            _LOGGER.error("Error logging in: %s", err)
            return None

    async def async_get_all_data(self) -> Dict[str, Any] | None:
        """Fetch data for all devices."""
        if not self.token:
            _LOGGER.error("Cannot fetch data: token is not set.")
            return None

        headers = {"Authorization": self.token}
        try:
            async with self._session.get(
                GET_ALL_DATA_URL, headers=headers, timeout=API_TIMEOUT
            ) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Get all data response: %s", data)

                if data.get("code") == 0 and isinstance(data.get("data"), list):
                    # Convert list of devices to a dict keyed by MAC for easy access
                    return {device["mac"]: device for device in data["data"]}
                
                # Handle token expiration
                if data.get("code") == 3:
                     _LOGGER.error("Token has expired or is invalid. Please re-authenticate.")
                     # We can implement re-authentication logic here in the future
                else:
                    _LOGGER.error("Failed to fetch device data: %s", data.get("message"))

                return None

        except aiohttp.ClientError as err:
            _LOGGER.error("Error fetching device data: %s", err)
            return None
