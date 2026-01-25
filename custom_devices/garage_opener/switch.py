"""Switch platform for Momentary Garage Switch integration."""
import logging
from typing import Any, Optional

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    CONF_TRIGGER_SWITCH,
    CONF_STATE_SENSOR,
    CONF_MOMENTARY_DURATION,
    DEFAULT_MOMENTARY_DURATION,
)
from .helpers import MomentaryHandler, StateTracker

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the Momentary Garage Switch platform."""
    # Get configuration from hass.data with a default empty list
    switch_configs = hass.data.get(DOMAIN, [])
    
    if not switch_configs:
        _LOGGER.debug("No Momentary Garage Switch configurations found")
        return

    switches = []
    for switch_config in switch_configs:
        switches.append(MomentaryGarageSwitch(hass, switch_config))

    async_add_entities(switches, True)


class MomentaryGarageSwitch(SwitchEntity):
    """Representation of a Momentary Garage Switch.
    
    This switch entity displays the actual door state from a binary sensor
    and triggers a momentary pulse on the physical garage switch when toggled.
    """

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        """Initialize the Momentary Garage Switch.
        
        Args:
            hass: Home Assistant instance
            config: Configuration dictionary for this switch
        """
        self.hass = hass
        self._name = config[CONF_NAME]
        self._trigger_switch = config[CONF_TRIGGER_SWITCH]
        self._state_sensor = config[CONF_STATE_SENSOR]
        self._duration = config.get(CONF_MOMENTARY_DURATION, DEFAULT_MOMENTARY_DURATION)
        
        self._is_on: Optional[bool] = None
        self._available = True
        
        # Initialize helper modules
        self._momentary_handler = MomentaryHandler(hass)
        self._state_tracker = StateTracker(
            hass, self._state_sensor, self._handle_state_update
        )

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        await super().async_added_to_hass()
        
        # Setup state tracking
        await self._state_tracker.async_setup()
        
        _LOGGER.info(
            "Momentary Garage Switch '%s' initialized (trigger: %s, sensor: %s)",
            self._name,
            self._trigger_switch,
            self._state_sensor,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        await super().async_will_remove_from_hass()
        
        # Cleanup
        await self._state_tracker.async_cleanup()
        await self._momentary_handler.cleanup()

    def _handle_state_update(self, is_on: bool) -> None:
        """Handle state updates from the binary sensor.
        
        Args:
            is_on: True if sensor is on (door open), False if off (door closed)
        """
        _LOGGER.debug(
            "State update for '%s': %s -> %s",
            self._name,
            self._is_on,
            is_on,
        )
        self._is_on = is_on
        self.schedule_update_ha_state()

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this switch."""
        return f"{DOMAIN}_{self._name.lower().replace(' ', '_')}"

    @property
    def is_on(self) -> Optional[bool]:
        """Return true if the switch is on (door is open)."""
        return self._is_on

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available and self._is_on is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        state_text = self._state_tracker.get_display_state()
        return {
            "state_text": state_text,
            "trigger_switch": self._trigger_switch,
            "state_sensor": self._state_sensor,
            "momentary_duration": self._duration,
        }

    @property
    def device_class(self) -> Optional[str]:
        """Return the device class of the switch."""
        # Return None for default switch behavior
        # Garage door switches don't have a specific device class
        return None

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        if self._is_on:
            return "mdi:garage-open"
        return "mdi:garage"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (trigger garage door).
        
        This triggers a momentary pulse on the physical garage switch,
        which will toggle the door state (open->close or close->open).
        """
        _LOGGER.info("Triggering garage door via '%s'", self._name)
        
        # Trigger the momentary pulse (non-blocking)
        await self._momentary_handler.trigger_momentary_nonblocking(
            self._trigger_switch, self._duration
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (trigger garage door).
        
        Since this is a toggle switch, turn_off does the same as turn_on:
        it triggers a momentary pulse to toggle the door state.
        """
        _LOGGER.info("Triggering garage door via '%s'", self._name)
        
        # Trigger the momentary pulse (non-blocking)
        await self._momentary_handler.trigger_momentary_nonblocking(
            self._trigger_switch, self._duration
        )

    async def async_update(self) -> None:
        """Update the entity.
        
        The state is primarily updated via the StateTracker callback,
        but this method can be called to force a refresh.
        """
        # State updates are handled by the StateTracker callback
        # This method is here for compatibility but doesn't need to do anything
        pass
