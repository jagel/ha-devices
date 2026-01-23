# Device Name Template

## Description
Brief description of what this device does.

## Hardware Requirements
- List all components needed
- Include part numbers if applicable
- Specify quantities

Example:
- 1x Arduino Uno
- 1x DHT22 Temperature/Humidity Sensor
- 1x 10kΩ resistor
- Jumper wires
- Breadboard

## Wiring Diagram

```
Arduino Uno    DHT22
-----------    -----
5V        -->  VCC
GND       -->  GND
D2        -->  DATA
```

(Include a Fritzing diagram or ASCII art diagram)

## Software Dependencies
- List all required libraries
- Specify minimum versions if needed

Example:
- PubSubClient (MQTT library)
- DHT sensor library
- ArduinoJson

## Installation

### 1. Hardware Setup
Step-by-step instructions for assembling the device.

### 2. Software Setup
1. Install required libraries
2. Configure WiFi credentials (if applicable)
3. Configure MQTT broker settings
4. Upload the code

### 3. Home Assistant Configuration
Instructions for setting up in Home Assistant.

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

## Payload Format

### State Message
```json
{
  "temperature": 22.5,
  "humidity": 45.0,
  "timestamp": 1234567890
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
  "unique_id": "device_name_001"
}
```

## Configuration

Update these values in the code:
```cpp
const char* ssid = "YOUR_WIFI_SSID";       // WiFi network name
const char* password = "YOUR_WIFI_PASS";   // WiFi password
const char* mqtt_server = "MQTT_BROKER_IP"; // MQTT broker address
const char* mqtt_user = "MQTT_USERNAME";    // MQTT username
const char* mqtt_pass = "MQTT_PASSWORD";    // MQTT password
```

## Troubleshooting

### Device won't connect to WiFi
- Check SSID and password
- Ensure WiFi is 2.4GHz (not 5GHz)
- Check signal strength

### Device won't connect to MQTT
- Verify broker IP address
- Check MQTT credentials
- Ensure broker is running

### No data in Home Assistant
- Check MQTT topics in MQTT explorer
- Verify discovery is enabled
- Check Home Assistant logs

## License
MIT License (inherited from repository)
