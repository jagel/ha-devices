"""Switch platform for Momentary Garage Switch integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import (
    DOMAIN,
    CONF_TRIGGER_SWITCH,
    CONF_STATE_SENSOR,
    ICON_GARAGE_OPEN,
    ICON_GARAGE_CLOSED,
)
from .helpers import SwitchHandler, StateTracker

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Garage Switch platform."""
    if DOMAIN not in hass.data or "config" not in hass.data[DOMAIN]:
        _LOGGER.error("Momentary Garage Switch not configured")
        return

    switches = []
    for switch_config in hass.data[DOMAIN]["config"]:
        switches.append(GarageSwitch(hass, switch_config))

    async_add_entities(switches, update_before_add=True)
    _LOGGER.debug("Added %d garage switches", len(switches))


class GarageSwitch(SwitchEntity, RestoreEntity):
    """Representation of a Garage Switch.
    
    This switch entity displays the actual door state from a binary sensor
    and triggers a momentary pulse on the physical garage switch when toggled.
    """

    _attr_should_poll = False
    _attr_assumed_state = False

    def __init__(self, hass: HomeAssistant, config: dict[str, Any]) -> None:
        """Initialize the Momentary Garage Switch.
        
        Args:
            hass: Home Assistant instance
            config: Configuration dictionary for this switch
        """
        self.hass = hass
        self._attr_name = config[CONF_NAME] # Name of the garage switch entity
        self._trigger_switch = config[CONF_TRIGGER_SWITCH] # Entity ID of the trigger switch 
        self._state_sensor = config[CONF_STATE_SENSOR] # Entity ID of the state binary sensor
        
        self._attr_unique_id = f"{DOMAIN}_{self._attr_name.lower().replace(' ', '_')}"
        self._attr_is_on: bool | None = None
        self._attr_available = True
        
        # Initialize helper modules
        self._switch_handler = SwitchHandler(hass)
        self._state_tracker = StateTracker(
            hass, self._state_sensor, self._handle_state_update
        )

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        await super().async_added_to_hass()
        
        # Restore previous state if available
        if (last_state := await self.async_get_last_state()) is not None:
            self._attr_is_on = last_state.state == "on"
        
        # Setup state tracking
        await self._state_tracker.async_setup()
        
        _LOGGER.info(
            "Garage Switch '%s' initialized (trigger: %s, sensor: %s)",
            self._attr_name,
            self._trigger_switch,
            self._state_sensor,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Run when entity will be removed from hass."""
        await super().async_will_remove_from_hass()
        
        # Cleanup
        await self._state_tracker.async_cleanup()
        await self._switch_handler.cleanup()

    def _handle_state_update(self, is_on: bool) -> None:
        """Handle state updates from the binary sensor.
        
        Args:
            is_on: True if sensor is on (door open), False if off (door closed)
        """
        _LOGGER.debug(
            "State update for '%s': %s -> %s",
            self._attr_name,
            self._attr_is_on,
            is_on,
        )
        self._attr_is_on = is_on
        self.schedule_update_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._attr_available and self._attr_is_on is not None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        state_text = self._state_tracker.get_display_state()
        return {
            "state_text": state_text,
            "trigger_switch": self._trigger_switch,
            "state_sensor": self._state_sensor,
            "integration": DOMAIN,
        }

    @property
    def device_class(self) -> str | None:
        """Return the device class of the switch."""
        # Garage door switches use the garage device class
        return "garage"

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return ICON_GARAGE_OPEN if self._attr_is_on else ICON_GARAGE_CLOSED

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on (trigger garage door).
        
        This triggers a pulse on the physical garage switch,
        which will toggle the door state (open->close or close->open).
        """
        _LOGGER.info("Triggering garage door via '%s'", self._name)
        
        # Trigger the trigger pulse (non-blocking)
        await self._switch_handler.trigger_nonblocking(
            self._trigger_switch
        )

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off (trigger garage door).
        
        Since this is a toggle switch, turn_off does the same as turn_on:
        it triggers a momentary pulse to toggle the door state.
        """
        _LOGGER.info("Triggering garage door via '%s'", self._name)
        
        # Trigger the momentary pulse (non-blocking)
        await self._switch_handler.trigger_nonblocking(
            self._trigger_switch
        )

    async def async_update(self) -> None:
        """Update the entity.
        
        The state is primarily updated via the StateTracker callback,
        but this method can be called to force a refresh.
        """
        # State updates are handled by the StateTracker callback
        # This method is here for compatibility but doesn't need to do anything
        pass
