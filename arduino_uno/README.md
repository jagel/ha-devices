# Arduino Uno Devices

This directory contains Home Assistant device implementations for Arduino Uno.

## Structure

Each device implementation should be in its own subdirectory:

```
arduino_uno/
├── temperature_sensor/
│   ├── README.md
│   ├── src/
│   └── platformio.ini (or .ino files)
├── motion_detector/
│   ├── README.md
│   ├── src/
│   └── platformio.ini (or .ino files)
└── ...
```

## Supported Languages

- C++
- Arduino C

## Getting Started

1. Create a new directory for your device implementation
2. Add a descriptive README.md explaining the device functionality
3. Implement your device code in the `src/` directory
4. Include wiring diagrams and configuration examples

## Communication Protocol

All devices should communicate with Home Assistant using MQTT protocol.

**Note**: Arduino Uno requires additional networking hardware (e.g., Ethernet Shield, WiFi Shield, or ESP8266/ESP32 module) to connect to the network and communicate via MQTT.

## Requirements

- Arduino IDE or PlatformIO
- MQTT library for Arduino
- Home Assistant MQTT integration configured
