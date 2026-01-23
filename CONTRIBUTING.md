# Contributing to Home Assistant Devices

Thank you for your interest in contributing to this project! This document provides guidelines for adding new device implementations to the repository.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Adding a New Device](#adding-a-new-device)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

Please be respectful and constructive in all interactions. We're building a community of makers and developers who help each other succeed.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your device implementation
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## Project Structure

The repository is organized by hardware platform:

```
ha-devices/
├── arduino_uno/      # Arduino Uno devices
├── raspberry_pi/     # Raspberry Pi devices
├── esp32/            # ESP32 devices
└── esp8266/          # ESP8266 devices
```

Each platform directory contains individual device implementations.

## Adding a New Device

### Step 1: Choose the Platform

Select the appropriate platform directory based on your hardware:
- `arduino_uno/` - For Arduino Uno based devices
- `raspberry_pi/` - For Raspberry Pi based devices (any model)
- `esp32/` - For ESP32 based devices
- `esp8266/` - For ESP8266 based devices

### Step 2: Create Device Directory

Create a new directory with a descriptive name using lowercase and underscores:

```bash
cd [platform_directory]
mkdir my_device_name
cd my_device_name
```

### Step 3: Required Files

Every device implementation should include:

#### README.md
Document your device with the following sections:
- **Description**: What does the device do?
- **Hardware Requirements**: List all components needed
- **Wiring Diagram**: Include a Fritzing diagram or clear description
- **Software Dependencies**: Libraries, packages, or tools required
- **Installation**: Step-by-step setup instructions
- **Configuration**: How to configure the device and Home Assistant
- **MQTT Topics**: Document all MQTT topics used
- **Payload Format**: Describe the data format sent/received
- **Troubleshooting**: Common issues and solutions

#### Source Code
Organize your code in a `src/` directory:

**For Arduino/ESP32/ESP8266:**
```
my_device_name/
├── README.md
├── platformio.ini (recommended) or .ino files
└── src/
    ├── main.cpp
    └── [additional files]
```

**For Raspberry Pi (Python):**
```
my_device_name/
├── README.md
├── requirements.txt
├── config.yaml (if needed)
└── src/
    ├── main.py
    └── [additional modules]
```

**For Raspberry Pi (Rust):**
```
my_device_name/
├── README.md
├── Cargo.toml
└── src/
    ├── main.rs
    └── [additional modules]
```

### Step 4: MQTT Implementation

All devices must use MQTT for communication with Home Assistant. Follow these guidelines:

#### Topic Naming Convention
```
homeassistant/[component]/[device_name]/[measurement]
```

Example:
```
homeassistant/sensor/living_room_temp/state
homeassistant/binary_sensor/front_door/state
homeassistant/switch/bedroom_light/set
```

#### Discovery
Implement MQTT Discovery to automatically configure devices in Home Assistant:

```json
{
  "name": "Living Room Temperature",
  "device_class": "temperature",
  "state_topic": "homeassistant/sensor/living_room_temp/state",
  "unit_of_measurement": "°C",
  "unique_id": "living_room_temp_001"
}
```

Publish to: `homeassistant/sensor/living_room_temp/config`

## Coding Standards

### General Guidelines
- Write clear, readable code with meaningful variable names
- Add comments for complex logic
- Follow the language-specific style guides
- Keep functions small and focused
- Handle errors gracefully

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Include docstrings for functions and classes
- Use virtual environments

### C/C++
- Use clear variable names (avoid single letters except for loops)
- Comment hardware pin assignments
- Define constants for magic numbers
- Free allocated memory

### Rust
- Follow Rust style guidelines (rustfmt)
- Use meaningful error types
- Write safe code (avoid unnecessary `unsafe`)
- Include inline documentation

## Testing Guidelines

### Hardware Testing
- Test all device functions thoroughly
- Verify MQTT connectivity
- Test edge cases (disconnections, invalid data, etc.)
- Document test results in your README

### Home Assistant Integration
- Verify the device appears in Home Assistant
- Test all controls and readings
- Check that state updates work correctly
- Verify MQTT Discovery works as expected

### Documentation Testing
- Follow your own installation instructions on a clean setup
- Verify all wiring diagrams are accurate
- Test all configuration examples

## Submitting Changes

### Pull Request Checklist
- [ ] Code is tested and working
- [ ] README.md is complete and accurate
- [ ] Wiring diagram is included
- [ ] MQTT topics are documented
- [ ] Code follows style guidelines
- [ ] Dependencies are documented
- [ ] Installation instructions are clear

### Pull Request Description
Include in your PR description:
1. What device does this implement?
2. What hardware is required?
3. What Home Assistant features does it provide?
4. Any special configuration needed?
5. Screenshots or photos of the working device (optional but appreciated!)

## Questions?

If you have questions about contributing, please open an issue and tag it with `question`.

Thank you for contributing to the Home Assistant Devices project!
