# ESP32 Devices

This directory contains Home Assistant device implementations for ESP32.

## Structure

Each device implementation should be in its own subdirectory:

```
esp32/
├── smart_switch/
│   ├── README.md
│   ├── src/
│   └── platformio.ini
├── weather_station/
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
4. Configure PlatformIO or Arduino IDE for ESP32
5. Include wiring diagrams and configuration examples

## Communication Protocol

All devices should communicate with Home Assistant using MQTT protocol.
WiFi connectivity is built-in to ESP32.

## Requirements

- ESP32 development board
- PlatformIO or Arduino IDE with ESP32 board support
- MQTT library for ESP32
- Home Assistant MQTT integration configured
