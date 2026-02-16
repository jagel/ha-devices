# jgl Garage Switch - Home Assistant Custom Integration

A production-ready, reusable Home Assistant custom integration for controlling garage doors with jgl switches and binary sensors.

## Features

- ✅ **jgl Switch Control**: Automatically pulses a physical switch (on → wait → off)
- ✅ **Real State Tracking**: Displays actual door state from binary sensor
- ✅ **Custom Display States**: Shows "open"/"close" instead of "on"/"off"
- ✅ **Multiple Instances**: Configure multiple garage doors via `configuration.yaml`
- ✅ **Reusable Helpers**: Generic helper modules for use in other integrations
- ✅ **Async/Await**: Full async implementation for optimal performance
- ✅ **Error Handling**: Graceful handling of unavailable sensors and switches

## Installation

> **Note**: This integration is located in the `custom_devices/garage_opener/` directory of this repository. When installing to Home Assistant, it should be placed in the `custom_components/jgl_garage_switch/` directory.

### Method 1: Manual Installation

1. Copy the entire contents of the `garage_opener` folder to your Home Assistant custom components directory:
   ```bash
   # Source (in this repo): custom_devices/garage_opener/
   # Destination (in Home Assistant): /config/custom_components/jgl_garage_switch/
   ```

2. Your directory structure should look like:
   ```
   /config/custom_components/
   └── jgl_garage_switch/
       ├── __init__.py
       ├── manifest.json
       ├── switch.py
       ├── const.py
       └── helpers/
           ├── __init__.py
           ├── jgl_handler.py
           └── state_tracker.py
   ```

3. Restart Home Assistant

### Method 2: HACS (Future)

This integration can be added to HACS custom repositories (coming soon).

## Configuration

Add the following to your `configuration.yaml`:

### Single Garage Door

```yaml
jgl_garage_switch:
  - name: "Garage Opener"
    trigger_switch: switch.genie_garage_opener_genie_garage_opener
    state_sensor: binary_sensor.0x001_contact
```

### Multiple Garage Doors

```yaml
jgl_garage_switch:
  - name: "Main Garage"
    trigger_switch: switch.main_garage_opener
    state_sensor: binary_sensor.main_garage_contact
  
  - name: "Side Garage"
    trigger_switch: switch.side_garage_opener
    state_sensor: binary_sensor.side_garage_contact
```

### Configuration Options

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `name` | Yes | - | Display name for the switch entity |
| `trigger_switch` | Yes | - | Entity ID of the physical garage switch to pulse |
| `state_sensor` | Yes | - | Entity ID of the binary sensor showing door state |

## How It Works

### Architecture

```
┌───────────────────────────────────────────────────┐
│  jglGarageSwitch Entity                           │
│  - Shows "open"/"close" based on binary sensor    │
│  - Triggers jgl pulse when toggled                │
└────────────┬────────────────────────────┬─────────┘
             │                            │
   ┌─────────▼──────────┐      ┌──────_───▼─────────┐
   │ StateTracker       │      │ jglHandler         │
   │ - Monitors sensor  │      │ - Pulses switch    │
   │ - Updates display  │      │ - Async control    │
   └────────────────────┘      └────────────────────┘
```

### State Flow

1. **Binary Sensor** (e.g., `binary_sensor.0x001_contact`):
   - `on` = door is open
   - `off` = door is closed

2. **StateTracker** monitors sensor changes:
   - Automatically updates switch state
   - Converts binary state to "open"/"close"

3. **User toggles switch** (via UI or automation):
   - Calls `async_turn_on()` or `async_turn_off()`

4. **jglHandler** triggers pulse:
   - Turn on `trigger_switch`
   - Wait for `jgl_duration` seconds
   - Turn off `trigger_switch`

5. **Physical garage door** responds:
   - Receives jgl pulse
   - Toggles state (open→close or close→open)

6. **Binary sensor** detects new state:
   - Loop back to step 1

## Usage

### In Home Assistant UI

1. Navigate to **Settings** → **Devices & Services** → **Entities**
2. Find `switch.garage_opener` (or your configured name)
3. Toggle the switch to open/close the garage door
4. State will automatically update when the door moves

### In Automations

```yaml
automation:
  - alias: "Open garage when arriving"
    trigger:
      - platform: zone
        entity_id: device_tracker.phone
        zone: zone.home
        event: enter
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.garage_opener
```

### In Scripts

```yaml
script:
  close_garage:
    sequence:
      - service: switch.turn_off
        target:
          entity_id: switch.garage_opener
      - delay: "00:00:30"
      - condition: state
        entity_id: switch.garage_opener
        state: "on"
      - service: notify.mobile_app
        data:
          message: "Warning: Garage door didn't close!"
```

## Reusing Helper Modules

The helper modules are designed to be reusable in other custom integrations.

### Using jglHandler in Your Integration

```python
from custom_components.jgl_garage_switch.helpers import jglHandler

class MyCustomSwitch(SwitchEntity):
    def __init__(self, hass):
        self._jgl = jglHandler(hass)
    
    async def async_turn_on(self, **kwargs):
        # Trigger a 2-second pulse
        await self._jgl.trigger_jgl(
            "switch.my_device", 
            duration=2.0
        )
```

### Using StateTracker in Your Integration

```python
from custom_components.jgl_garage_switch.helpers import StateTracker

class MyCustomSwitch(SwitchEntity):
    def __init__(self, hass):
        self._tracker = StateTracker(
            hass,
            "binary_sensor.my_sensor",
            self._on_state_change
        )
    
    async def async_added_to_hass(self):
        await self._tracker.async_setup()
    
    def _on_state_change(self, is_on: bool):
        # Handle state updates
        self._is_on = is_on
        self.schedule_update_ha_state()
```

## Troubleshooting

### Switch Not Appearing

1. Check logs for errors:
   ```bash
   grep "jgl_garage_switch" /config/home-assistant.log
   ```

2. Verify configuration:
   - Check `configuration.yaml` syntax
   - Ensure entity IDs exist and are correct
   - Restart Home Assistant after config changes

### State Not Updating

1. **Check binary sensor**:
   - Verify `binary_sensor.0x001_contact` exists
   - Check if sensor state changes when door moves

2. **Check logs**:
   ```
   [custom_components.jgl_garage_switch.helpers.state_tracker] State changed
   ```

3. **Entity unavailable**:
   - Sensor might be offline or returning `unavailable`
   - Check sensor device connectivity

### jgl Pulse Not Working

1. **Check trigger switch**:
   - Verify `switch.genie_garage_opener_genie_garage_opener` exists
   - Test switch manually to ensure it controls the garage

2. **Duration too short**:
   - Some garage openers need longer pulses
   - Try increasing `jgl_duration` to 1.5 or 2 seconds

3. **Check logs**:
   ```
   [custom_components.jgl_garage_switch.helpers.jgl_handler] Triggering jgl switch
   ```

### Multiple Triggers

- If the door triggers multiple times, ensure no automations are also toggling the trigger switch

## Advanced Configuration

### Custom Icon

Add a customization in `configuration.yaml`:

```yaml
homeassistant:
  customize:
    switch.garage_opener:
      icon: mdi:garage-variant
```

### Template Sensor for Open/Close Text

```yaml
template:
  - sensor:
      - name: "Garage Status"
        state: "{{ state_attr('switch.garage_opener', 'state_text') }}"
        icon: "{{ state_attr('switch.garage_opener', 'icon') }}"
```

## Development

### Project Structure

```
custom_devices/garage_opener/
├── __init__.py              # Integration setup
├── manifest.json            # Integration metadata
├── const.py                 # Constants and schema
├── switch.py                # Main switch entity
└── helpers/
    ├── __init__.py          # Helper exports
    ├── jgl_handler.py # Reusable jgl logic
    └── state_tracker.py     # Reusable state tracking
```

### Key Design Principles

1. **Separation of Concerns**: Business logic isolated in helper modules
2. **Reusability**: Helpers can be imported by other integrations
3. **Async First**: Full async/await for non-blocking operations
4. **Error Handling**: Graceful degradation when sensors unavailable
5. **Configuration Driven**: Multiple instances via YAML config

### Testing

Create a test environment:

```yaml
# configuration.yaml
jgl_garage_switch:
  - name: "Test Garage"
    trigger_switch: input_boolean.test_trigger
    state_sensor: input_boolean.test_sensor
    jgl_duration: 0.5

input_boolean:
  test_trigger:
    name: Test Trigger
  test_sensor:
    name: Test Sensor
```

## Example Hardware Setups

### With Shelly Relay

```yaml
jgl_garage_switch:
  - name: "Garage Door"
    trigger_switch: switch.shelly_garage_relay
    state_sensor: binary_sensor.garage_door_contact
    jgl_duration: 1
```

### With Sonoff Switch

```yaml
jgl_garage_switch:
  - name: "Garage Door"
    trigger_switch: switch.sonoff_garage
    state_sensor: binary_sensor.garage_sensor
    jgl_duration: 1
```

### With Zigbee Devices

```yaml
jgl_garage_switch:
  - name: "Garage Door"
    trigger_switch: switch.zigbee_relay_garage
    state_sensor: binary_sensor.aqara_contact_garage
    jgl_duration: 1
```

## Security Considerations

### Door State Verification

Always verify door state before triggering:

```yaml
automation:
  - alias: "Close garage at night - safe"
    trigger:
      - platform: time
        at: "22:00:00"
    condition:
      - condition: state
        entity_id: switch.garage_opener
        state: "on"  # Only if door is open
    action:
      - service: switch.turn_off
        target:
          entity_id: switch.garage_opener
```

### Notification on State Change

```yaml
automation:
  - alias: "Notify on garage state change"
    trigger:
      - platform: state
        entity_id: switch.garage_opener
    action:
      - service: notify.mobile_app
        data:
          message: >
            Garage door is now {{ state_attr('switch.garage_opener', 'state_text') }}
```

## FAQ

**Q: Can I use this with covers instead of switches?**

A: This integration creates a switch entity. To use with Home Assistant's cover UI, you can create a template cover that references this switch.

**Q: Does this work with any garage door opener?**

A: Yes, as long as you have:
1. A switch/relay that can trigger the opener
2. A binary sensor (contact sensor) that detects door position

**Q: Can I trigger the door from voice assistants?**

A: Yes! Once configured, you can use Google Assistant, Alexa, or Siri to control the switch.

**Q: What happens if the binary sensor fails?**

A: The switch will show as "unavailable" but can still trigger the door. You just won't see the current state.

## Contributing

Contributions welcome! This integration is designed to be extended.

### Ideas for Enhancement

- [ ] Add MQTT discovery support
- [ ] Add timer to auto-close after X minutes
- [ ] Add safety warnings if door left open
- [ ] Create template cover wrapper
- [ ] Add configuration flow (UI config)

## License

MIT License (inherited from repository)

## Credits

- Created for the [ha-devices](https://github.com/jagel/ha-devices) repository
- Compatible with Home Assistant 2023.x and newer

## Support

For issues or questions:
- GitHub Issues: [ha-devices/issues](https://github.com/jagel/ha-devices/issues)
- Home Assistant Community: Tag with `jgl_garage_switch`
