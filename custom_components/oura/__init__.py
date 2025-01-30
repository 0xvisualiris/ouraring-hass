'''The Oura Ring integration.'''
from __future__ import annotations
import logging
from datetime import timedelta
from aiohttp import ClientSession
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_BASE_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    '''Set up the Oura Ring component.'''
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    '''Set up Oura Ring from a config entry.'''
    session = async_get_clientsession(hass)
    coordinator = OuraDataUpdateCoordinator(
        hass,
        session,
        entry.data[CONF_ACCESS_TOKEN],
        entry.entry_id
    )
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    hass.async_create_task(hass.config_entries.async_forward_entry_setups(entry, PLATFORMS))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    '''Unload a config entry.'''
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok

class OuraDataUpdateCoordinator(DataUpdateCoordinator):
    '''Class to manage fetching data from Oura Ring API.'''

    def __init__(
        self, hass: HomeAssistant, session: ClientSession, access_token: str, entry_id: str
    ) -> None:
        '''Initialize the coordinator.'''
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry_id}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self._session = session
        self._access_token = access_token
        self._headers = {"Authorization": f"Bearer {access_token}"}

    async def _async_update_data(self) -> dict:
        '''Fetch data from Oura API.'''
        try:
            data = {}
            endpoints = {
                "activity_score": "usercollection/daily_activity",
                "readiness_score": "usercollection/daily_readiness",
                "sleep_score": "usercollection/daily_sleep",
                "cardiovascular_age": "usercollection/daily_cardiovascular_age",
                "resilience": "usercollection/daily_resilience",
                "spo2": "usercollection/daily_spo2",
                "stress": "usercollection/daily_stress",
                "heartrate": "usercollection/heartrate",
                "rest_mode": "usercollection/rest_mode_period",
            }
            
            for key, endpoint in endpoints.items():
                url = f"{API_BASE_URL}/{endpoint}"
                _LOGGER.debug("Fetching Oura data from: %s", url)
                
                async with self._session.get(url, headers=self._headers) as resp:
                    if resp.status != 200:
                        _LOGGER.error(
                            "API error for %s: %s - %s",
                            endpoint,
                            resp.status,
                            await resp.text()
                        )
                        continue
                    
                    result = await resp.json()
                    _LOGGER.debug("API response for %s: %s", endpoint, result)
                    
                    if "data" in result and result["data"]:
                        data[key] = result["data"][0].get("score", None)
                    else:
                        _LOGGER.warning("No data returned for %s. Full response: %s", endpoint, result)
                        data[key] = None
            
            return data
            
        except Exception as err:
            _LOGGER.error("Error fetching data from Oura API: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err
