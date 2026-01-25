"""Reusable momentary switch handler for Home Assistant integrations."""
import asyncio
import logging
from typing import Optional

from homeassistant.core import HomeAssistant
from homeassistant.const import (
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF,
)

_LOGGER = logging.getLogger(__name__)


class MomentaryHandler:
    """Reusable momentary switch handler.
    
    This class provides a generic way to trigger a momentary switch pulse
    (turn on, wait, turn off) for any Home Assistant switch entity.
    Can be reused across different integrations.
    """

    def __init__(self, hass: HomeAssistant):
        """Initialize the momentary handler.
        
        Args:
            hass: Home Assistant instance
        """
        self.hass = hass
        self._active_tasks = set()

    async def trigger_momentary(
        self, entity_id: str, duration: float = 1.0
    ) -> bool:
        """Turn on entity, wait for duration, then turn off.
        
        Args:
            entity_id: The entity ID of the switch to trigger
            duration: How long to keep the switch on (in seconds)
            
        Returns:
            bool: True if successful, False if there was an error
        """
        try:
            _LOGGER.debug(
                "Triggering momentary switch %s for %.1f seconds",
                entity_id,
                duration,
            )

            # Turn on the switch
            await self.hass.services.async_call(
                "switch",
                SERVICE_TURN_ON,
                {"entity_id": entity_id},
                blocking=True,
            )

            # Wait for the specified duration
            await asyncio.sleep(duration)

            # Turn off the switch
            await self.hass.services.async_call(
                "switch",
                SERVICE_TURN_OFF,
                {"entity_id": entity_id},
                blocking=True,
            )

            _LOGGER.debug("Momentary switch %s completed successfully", entity_id)
            return True

        except Exception as e:
            _LOGGER.error(
                "Error triggering momentary switch %s: %s",
                entity_id,
                str(e),
            )
            return False

    async def trigger_momentary_nonblocking(
        self, entity_id: str, duration: float = 1.0
    ) -> None:
        """Trigger momentary switch without blocking.
        
        Creates a background task to handle the momentary pulse.
        
        Args:
            entity_id: The entity ID of the switch to trigger
            duration: How long to keep the switch on (in seconds)
        """
        task = asyncio.create_task(self.trigger_momentary(entity_id, duration))
        self._active_tasks.add(task)
        task.add_done_callback(self._active_tasks.discard)

    async def cleanup(self) -> None:
        """Cancel all active momentary tasks."""
        if self._active_tasks:
            _LOGGER.debug("Cancelling %d active momentary tasks", len(self._active_tasks))
            for task in self._active_tasks:
                task.cancel()
            # Wait for all tasks to complete
            await asyncio.gather(*self._active_tasks, return_exceptions=True)
            self._active_tasks.clear()
