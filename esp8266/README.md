# ESP8266 Devices

This directory contains Home Assistant device implementations for ESP8266.

## Structure

Each device implementation should be in its own subdirectory:

```
esp8266/
├── relay_controller/
│   ├── README.md
│   ├── src/
│   └── platformio.ini
├── door_sensor/
│   ├── README.md
│   ├── src/
│   └── platformio.ini
└── ...
```

## Supported Languages

- C++
- Arduino C

## Getting Started

1. Create a new directory for your device implementation
2. Add a descriptive README.md explaining the device functionality
3. Implement your device code in the `src/` directory
4. Configure PlatformIO or Arduino IDE for ESP8266
5. Include wiring diagrams and configuration examples

## Communication Protocol

All devices should communicate with Home Assistant using MQTT protocol.
WiFi connectivity is built-in to ESP8266.

## Requirements

- ESP8266 development board (NodeMCU, Wemos D1 Mini, etc.)
- PlatformIO or Arduino IDE with ESP8266 board support
- MQTT library for ESP8266
- Home Assistant MQTT integration configured
