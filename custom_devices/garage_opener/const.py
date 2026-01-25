"""Constants for the Momentary Garage Switch integration."""
import voluptuous as vol
from homeassistant.const import CONF_NAME
import homeassistant.helpers.config_validation as cv

# Domain
DOMAIN = "momentary_garage_switch"

# Configuration keys
CONF_TRIGGER_SWITCH = "trigger_switch"
CONF_STATE_SENSOR = "state_sensor"
CONF_MOMENTARY_DURATION = "momentary_duration"

# Defaults
DEFAULT_MOMENTARY_DURATION = 1

# Configuration schema
SWITCH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_TRIGGER_SWITCH): cv.entity_id,
        vol.Required(CONF_STATE_SENSOR): cv.entity_id,
        vol.Optional(
            CONF_MOMENTARY_DURATION, default=DEFAULT_MOMENTARY_DURATION
        ): vol.All(vol.Coerce(float), vol.Range(min=0.1, max=60)),
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [SWITCH_SCHEMA])}, extra=vol.ALLOW_EXTRA
)
