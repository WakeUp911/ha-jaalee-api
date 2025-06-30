"""Config flow for Jaalee API."""
import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import JaaleeApiClient
from .const import CONF_EMAIL, CONF_TOKEN, DOMAIN

_LOGGER = logging.getLogger(__name__)

class JaaleeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Jaalee API."""

    VERSION = 1
    
    def __init__(self) -> None:
        """Initialize the config flow."""
        self.email: str | None = None

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Handle the initial step."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            self.email = user_input[CONF_EMAIL]
            
            # Check if an entry with this email already exists
            await self.async_set_unique_id(self.email)
            self._abort_if_unique_id_configured()

            api_client = JaaleeApiClient(self.hass, email=self.email)
            if await api_client.async_get_code():
                return await self.async_step_code()
            
            errors["base"] = "cannot_get_code"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_EMAIL): str}),
            errors=errors,
        )

    async def async_step_code(
        self, user_input: Dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """Handle the verification code step."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            code = user_input["code"]
            api_client = JaaleeApiClient(self.hass, email=self.email)
            
            token = await api_client.async_login(code)
            if token:
                return self.async_create_entry(
                    title=self.email,
                    data={
                        CONF_EMAIL: self.email,
                        CONF_TOKEN: token,
                    },
                )
            
            errors["base"] = "invalid_code"

        return self.async_show_form(
            step_id="code",
            data_schema=vol.Schema({vol.Required("code"): str}),
            errors=errors,
        )
