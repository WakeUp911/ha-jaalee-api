"""The Jaalee API integration."""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import JaaleeApiClient
from .const import CONF_EMAIL, CONF_TOKEN, DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=2) # Respecting the 1-minute API limit

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Jaalee API from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    email = entry.data[CONF_EMAIL]
    token = entry.data[CONF_TOKEN]

    api_client = JaaleeApiClient(hass, email=email, token=token)

    async def async_update_data():
        """Fetch data from API endpoint."""
        try:
            data = await api_client.async_get_all_data()
            if data is None:
                raise UpdateFailed("Failed to fetch data from Jaalee API")
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="jaalee_api_coordinator",
        update_method=async_update_data,
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
