"""Reusable momentary switch handler for Home Assistant integrations."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.const import Platform, SERVICE_TURN_ON, SERVICE_TURN_OFF
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)


class SwitchHandler:
    """Switch handler.
    
    This class provides a generic way to trigger a switch pulse
    (always turn on) for any Home Assistant switch entity.
    """

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the momentary handler.
        
        Args:
            hass: Home Assistant instance
        """
        self.hass = hass
        self._active_tasks: set[asyncio.Task[Any]] = set()

    async def trigger(
        self, entity_id: str
    ) -> bool:
        """Turn on entity.
        
        Args:
            entity_id: The entity ID of the switch to trigger
            
        Returns:
            bool: True if successful, False if there was an error
        """
        try:
            _LOGGER.debug("Switch %s turned on", entity_id,)

            # Validate entity exists
            if not self.hass.states.get(entity_id):
                raise HomeAssistantError(f"Entity {entity_id} not found")
            
            # Turn on the switch
            await self.hass.services.async_call(
                Platform.SWITCH,
                SERVICE_TURN_ON,
                {"entity_id": entity_id},
                blocking=True,
            )


            _LOGGER.debug("Trigger switch %s completed successfully", entity_id)
            return True

        except asyncio.CancelledError:
            _LOGGER.debug("Trigger switch %s task was cancelled", entity_id)
            return False
        except Exception as e:
            _LOGGER.error(
                "Error triggering switch %s: %s",
                entity_id,
                str(e),
            )
            return False

    async def trigger_nonblocking(
        self, entity_id: str
    ) -> None:
        """Trigger switch without blocking.
        
        Creates a background task to handle the pulse.
        
        Args:
            entity_id: The entity ID of the switch to trigger
        """
        task = asyncio.create_task(self.trigger(entity_id))
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
