# Home Assistant Devices

A monorepo containing IoT device implementations for Home Assistant using MQTT protocol. This repository supports multiple hardware platforms including Arduino, Raspberry Pi, ESP32, and ESP8266.

## Overview

This monorepo contains device implementations that communicate with Home Assistant using MQTT. Each device platform has its own directory with specific device implementations.

## Repository Structure

```
ha-devices/
├── arduino_uno/          # Arduino Uno device implementations
│   ├── README.md
│   └── [device_name]/    # Individual device folders
├── raspberry_pi/         # Raspberry Pi device implementations
│   ├── README.md
│   └── [device_name]/    # Individual device folders
├── esp32/                # ESP32 device implementations
│   ├── README.md
│   └── [device_name]/    # Individual device folders
├── esp8266/              # ESP8266 device implementations
│   ├── README.md
│   └── [device_name]/    # Individual device folders
├── .gitignore
├── LICENSE
└── README.md
```

## Supported Platforms

### Arduino Uno
- **Languages**: C++, Arduino C
- **Use Cases**: Basic sensors, switches, and simple automation devices
- **Directory**: `arduino_uno/`

### Raspberry Pi
- **Languages**: Python, Rust, C++
- **Use Cases**: Complex automation, cameras, AI/ML processing, multi-sensor hubs
- **Directory**: `raspberry_pi/`

### ESP32
- **Languages**: C++, Arduino C
- **Use Cases**: WiFi-enabled sensors, switches, smart home devices
- **Directory**: `esp32/`

### ESP8266
- **Languages**: C++, Arduino C
- **Use Cases**: Low-cost WiFi-enabled sensors and switches
- **Directory**: `esp8266/`

## Getting Started

1. **Choose your platform**: Navigate to the appropriate device platform directory
2. **Review platform README**: Each platform directory has specific setup instructions
3. **Create your device**: Follow the structure guidelines to implement your device
4. **Test with Home Assistant**: Configure MQTT integration in Home Assistant

## Communication Protocol

All devices in this repository use **MQTT** (Message Queuing Telemetry Transport) to communicate with Home Assistant. Ensure you have:

- MQTT broker installed and configured (e.g., Mosquitto)
- Home Assistant MQTT integration enabled
- Proper network connectivity between devices and the MQTT broker

## Contributing

To add a new device implementation:

1. Choose the appropriate platform directory
2. Create a new subdirectory with a descriptive name
3. Include a README.md with:
   - Device description and features
   - Hardware requirements and wiring diagram
   - Software dependencies
   - Configuration instructions
   - MQTT topics and payloads
4. Add your implementation code
5. Test thoroughly with Home Assistant

## Directory Naming Convention

- Use lowercase with underscores for directory names
- Be descriptive but concise (e.g., `temperature_sensor`, `motion_detector`)
- Avoid version numbers in directory names

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please use the GitHub issue tracker.
