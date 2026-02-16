"""The Momentary Garage Switch integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    CONF_TRIGGER_SWITCH,
    CONF_STATE_SENSOR,
    SERVICE_TRIGGER
)

_LOGGER = logging.getLogger(__name__)

# Configuration schema
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required(CONF_NAME): cv.string,
                        vol.Required(CONF_TRIGGER_SWITCH): cv.entity_id,
                        vol.Required(CONF_STATE_SENSOR): cv.entity_id,
                    }
                )
            ],
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Jgl Garage Switch component."""
    if DOMAIN not in config:
        return True

    _LOGGER.debug("Setting up %s integration", DOMAIN)

    # Initialize domain data
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Store config in hass.data for the switch platform to access
    hass.data[DOMAIN]["config"] = config[DOMAIN]

    # Load the switch platform
    await discovery.async_load_platform(
        hass,
        Platform.SWITCH,
        DOMAIN,
        {},
        config,
    )

    # Register services
    async def async_trigger_service(call: ServiceCall) -> None:
        """Handle trigger service call."""
        entity_id = call.data.get("entity_id")
        if entity_id:
            # Find the corresponding switch entity and trigger it
            switch_entity = hass.states.get(entity_id)
            if switch_entity:
                await hass.services.async_call(
                    Platform.SWITCH,
                    "turn_on",
                    {"entity_id": entity_id},
                    blocking=True,
                )

    hass.services.async_register(
        DOMAIN,
        SERVICE_TRIGGER,
        async_trigger_service,
        vol.Schema({vol.Required("entity_id"): cv.entity_id}),
    )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry (for future config flow support)."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True