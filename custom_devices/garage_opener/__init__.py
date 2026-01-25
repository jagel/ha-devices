"""The Momentary Garage Switch integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Momentary Garage Switch component."""
    if DOMAIN not in config:
        return True

    _LOGGER.debug("Setting up Momentary Garage Switch integration")

    # Store configuration in hass.data
    hass.data[DOMAIN] = config[DOMAIN]

    # Load the switch platform
    await hass.helpers.discovery.async_load_platform("switch", DOMAIN, {}, config)

    return True
