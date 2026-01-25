"""The Momentary Garage Switch integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONFIG_SCHEMA

_LOGGER = logging.getLogger(__name__)

# Expose CONFIG_SCHEMA for Home Assistant to validate configuration
CONFIG_SCHEMA = CONFIG_SCHEMA  # noqa: F811


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Momentary Garage Switch component."""
    if DOMAIN not in config:
        return True

    _LOGGER.debug("Setting up Momentary Garage Switch integration")

    # Configuration is already validated by Home Assistant using CONFIG_SCHEMA
    # Store configuration in hass.data
    hass.data[DOMAIN] = config[DOMAIN]

    # Load the switch platform
    # Note: Using async_load_platform for YAML-configured integrations.
    # For config entry-based integrations, use async_forward_entry_setups instead.
    await hass.helpers.discovery.async_load_platform("switch", DOMAIN, {}, config)

    return True
