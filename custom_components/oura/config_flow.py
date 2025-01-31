"""Config flow for Oura Ring integration."""
from __future__ import annotations

import logging
from typing import Any

from aiohttp import ClientError, ClientSession
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, API_BASE_URL

_LOGGER = logging.getLogger(__name__)

CONF_SENSORS = "sensors"

SENSOR_OPTIONS = {
    "sleep": "Sleep",
    "readiness": "Readiness",
    "activity": "Activity",
    "cardiovascular_age": "Cardiovascular Age",
    "resilience": "Resilience",
    "spo2": "SpO2",
    "stress": "Stress",
    "heartrate": "Heart Rate",
    "rest_mode": "Rest Mode",
}

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCESS_TOKEN): str,
    }
)

STEP_SENSOR_SELECTION_SCHEMA = vol.Schema(
    {
        vol.Optional(sensor, default=True): bool
        for sensor in SENSOR_OPTIONS.keys()
    }
)


class OuraFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Oura Ring."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            valid = await self._test_credentials(
                session, user_input[CONF_ACCESS_TOKEN]
            )

            if valid:
                self.access_token = user_input[CONF_ACCESS_TOKEN]
                return await self.async_step_sensors()

            errors["base"] = "auth"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Allow users to select which sensors to enable."""
        if user_input is not None:
            selected_sensors = [
                sensor for sensor, enabled in user_input.items() if enabled
            ]
            return self.async_create_entry(
                title="Oura Ring",
                data={CONF_ACCESS_TOKEN: self.access_token, CONF_SENSORS: selected_sensors},
            )

        return self.async_show_form(
            step_id="sensors",
            data_schema=STEP_SENSOR_SELECTION_SCHEMA,
        )

    async def _test_credentials(self, session: ClientSession, access_token: str) -> bool:
        """Test if the credentials are valid."""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{API_BASE_URL}/usercollection/personal_info"

            async with session.get(url, headers=headers) as response:
                if response.status == 401:
                    return False
                response.raise_for_status()
                return True

        except ClientError:
            return False
