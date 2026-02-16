"""Constants for the Momentary Garage Switch integration."""
from __future__ import annotations

from homeassistant.const import CONF_NAME

# Domain
DOMAIN = "jgl_garage_switch"

# Configuration keys
CONF_TRIGGER_SWITCH = "trigger_switch"
CONF_STATE_SENSOR = "state_sensor"
CONF_MOMENTARY_DURATION = "momentary_duration"

# Service names
SERVICE_TRIGGER = "trigger"

# Icons
ICON_GARAGE_OPEN = "mdi:garage-open"
ICON_GARAGE_CLOSED = "mdi:garage"
