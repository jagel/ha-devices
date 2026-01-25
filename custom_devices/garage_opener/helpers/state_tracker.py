"""Reusable state tracking from binary sensor for Home Assistant integrations."""
import logging
from typing import Callable, Optional

from homeassistant.core import HomeAssistant, State, callback
from homeassistant.const import STATE_ON, STATE_OFF, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.helpers.event import async_track_state_change_event

_LOGGER = logging.getLogger(__name__)


class StateTracker:
    """Reusable state tracking from binary sensor.
    
    This class monitors a binary sensor and provides state change callbacks.
    Can be reused across different integrations that need to track sensor states.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        sensor_entity_id: str,
        callback_func: Callable[[bool], None],
    ):
        """Initialize the state tracker.
        
        Args:
            hass: Home Assistant instance
            sensor_entity_id: Entity ID of the binary sensor to track
            callback_func: Function to call when state changes (receives bool: True=on, False=off)
        """
        self.hass = hass
        self.sensor_entity_id = sensor_entity_id
        self._callback = callback_func
        self._current_state: Optional[bool] = None
        self._unsub_state_listener = None

    async def async_setup(self) -> None:
        """Setup event listeners for state changes."""
        _LOGGER.debug("Setting up state tracker for %s", self.sensor_entity_id)

        # Get initial state
        await self._update_current_state()

        # Subscribe to state changes
        self._unsub_state_listener = async_track_state_change_event(
            self.hass, [self.sensor_entity_id], self._async_state_changed
        )

    async def _update_current_state(self) -> None:
        """Update the current state from the sensor."""
        state = self.hass.states.get(self.sensor_entity_id)
        if state is not None:
            new_state = self._parse_state(state)
            if new_state != self._current_state:
                self._current_state = new_state
                if self._callback and new_state is not None:
                    self._callback(new_state)

    @callback
    def _async_state_changed(self, event) -> None:
        """Handle state changes from the binary sensor."""
        new_state = event.data.get("new_state")
        if new_state is None:
            return

        parsed_state = self._parse_state(new_state)
        
        if parsed_state != self._current_state:
            _LOGGER.debug(
                "State changed for %s: %s -> %s",
                self.sensor_entity_id,
                self._current_state,
                parsed_state,
            )
            self._current_state = parsed_state
            
            if self._callback and parsed_state is not None:
                self._callback(parsed_state)

    def _parse_state(self, state: State) -> Optional[bool]:
        """Parse state object to boolean.
        
        Args:
            state: Home Assistant State object
            
        Returns:
            True if on/open, False if off/closed, None if unavailable/unknown
        """
        if state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            _LOGGER.warning(
                "Sensor %s is %s",
                self.sensor_entity_id,
                state.state,
            )
            return None
        
        return state.state == STATE_ON

    def get_current_state(self) -> Optional[bool]:
        """Get current sensor state.
        
        Returns:
            True if on, False if off, None if unavailable
        """
        return self._current_state

    def get_display_state(self) -> str:
        """Convert binary state to display text.
        
        Returns:
            "open" if True, "close" if False, "unavailable" if None
        """
        if self._current_state is None:
            return "unavailable"
        return "open" if self._current_state else "close"

    async def async_cleanup(self) -> None:
        """Clean up state listeners."""
        if self._unsub_state_listener:
            _LOGGER.debug("Cleaning up state tracker for %s", self.sensor_entity_id)
            self._unsub_state_listener()
            self._unsub_state_listener = None
