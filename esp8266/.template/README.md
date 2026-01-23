# Device Name Template

## Description
Brief description of what this device does.

## Hardware Requirements
- List all components needed
- Include part numbers if applicable

Example:
- 1x ESP8266 Development Board (NodeMCU, Wemos D1 Mini, etc.)
- 1x DHT22 Temperature/Humidity Sensor
- 1x 10kΩ resistor
- Jumper wires
- Micro USB cable for power

## Wiring Diagram

```
ESP8266 (D1 Mini)    DHT22
-----------------    -----
3.3V            -->  VCC
GND             -->  GND
D4 (GPIO 2)     -->  DATA
```

(Include a pinout diagram for your specific board)

## Software Dependencies
- PubSubClient (MQTT library)
- DHT sensor library
- ESP8266WiFi library (built-in)
- ArduinoJson

## Installation

### 1. Hardware Setup
Step-by-step instructions for assembling the device.

### 2. PlatformIO Setup (Recommended)
1. Install PlatformIO IDE or Core
2. Open this directory in PlatformIO
3. Update `platformio.ini` with your settings
4. Build and upload: `pio run -t upload`

Example `platformio.ini`:
```ini
[env:d1_mini]
platform = espressif8266
board = d1_mini
framework = arduino
lib_deps = 
    knolleary/PubSubClient@^2.8
    adafruit/DHT sensor library@^1.4.4
    bblanchon/ArduinoJson@^6.21.0
monitor_speed = 115200
```

### 3. Arduino IDE Setup
1. Install ESP8266 board support
2. Install required libraries via Library Manager
3. Open `src/main.cpp` (rename to .ino if needed)
4. Update WiFi and MQTT credentials
5. Select your ESP8266 board and port
6. Upload

### 4. Configuration
Update credentials in the code:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "MQTT_BROKER_IP";
const char* mqtt_user = "MQTT_USERNAME";
const char* mqtt_pass = "MQTT_PASSWORD";
```

## MQTT Topics

### State Topic
```
homeassistant/sensor/device_name/state
```
Publishes sensor readings in JSON format.

### Configuration Topic (Discovery)
```
homeassistant/sensor/device_name/config
```
Auto-discovery configuration payload.

### Command Topic (for controllable devices)
```
homeassistant/switch/device_name/set
```
Receives commands from Home Assistant.

## Payload Format

### State Message
```json
{
  "temperature": 22.5,
  "humidity": 45.0,
  "rssi": -65
}
```

### Discovery Message
```json
{
  "name": "Device Name",
  "device_class": "temperature",
  "state_topic": "homeassistant/sensor/device_name/state",
  "unit_of_measurement": "°C",
  "value_template": "{{ value_json.temperature }}",
  "unique_id": "device_name_001",
  "device": {
    "identifiers": ["device_name_001"],
    "name": "Device Name",
    "model": "ESP8266",
    "manufacturer": "DIY"
  }
}
```

## Features

- **WiFi Connectivity**: Built-in WiFi for network access
- **Low Power**: Energy-efficient for battery operation
- **MQTT Auto-Discovery**: Automatic configuration in Home Assistant
- **Compact Size**: Small form factor for tight spaces

## Troubleshooting

### Device won't connect to WiFi
- Ensure WiFi is 2.4GHz only (ESP8266 doesn't support 5GHz)
- Check SSID and password
- Verify signal strength
- Check serial monitor for connection status

### Device won't connect to MQTT
- Verify broker IP address and port
- Check MQTT credentials
- Ensure broker allows connections from the network
- Check firewall settings

### Device keeps rebooting
- Check power supply (ESP8266 needs stable 5V/500mA+)
- Verify wiring connections
- Check for short circuits
- Review serial monitor for error messages
- Ensure GPIO pins aren't overloaded

### Flash fails
- Try different USB cable
- Press and hold FLASH button during upload
- Reduce upload speed in platformio.ini: `upload_speed = 115200`
- Check drivers for CH340/CP2102 chip

### No data in Home Assistant
- Check MQTT topics with MQTT Explorer
- Verify discovery is enabled in HA
- Check that device is publishing data (serial monitor)
- Restart Home Assistant MQTT integration

## Serial Monitor
Connect via USB and open serial monitor at 115200 baud to see debug output:
- WiFi connection status
- MQTT publish/subscribe status
- Sensor readings
- Error messages
- IP address

## Power Considerations

ESP8266 power consumption:
- Active WiFi: ~70-80mA
- Modem sleep: ~15mA
- Deep sleep: ~20μA

For battery operation, implement deep sleep between readings.

## License
MIT License (inherited from repository)
