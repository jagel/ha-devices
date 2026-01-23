# Raspberry Pi Devices

This directory contains Home Assistant device implementations for Raspberry Pi.

## Structure

Each device implementation should be in its own subdirectory:

```
raspberry_pi/
├── climate_monitor/
│   ├── README.md
│   ├── src/
│   ├── requirements.txt (Python)
│   └── config.yaml
├── camera_feed/
│   ├── README.md
│   ├── src/
│   ├── requirements.txt (Python)
│   └── config.yaml
└── ...
```

## Supported Languages

- Python
- Rust
- C++

## Getting Started

1. Create a new directory for your device implementation
2. Add a descriptive README.md explaining the device functionality
3. Implement your device code in the `src/` directory
4. Include dependencies file (requirements.txt for Python, Cargo.toml for Rust)
5. Provide configuration examples

## Communication Protocol

All devices should communicate with Home Assistant using MQTT protocol.

## Requirements

- Raspberry Pi (any model)
- MQTT broker accessible from the network
- Home Assistant MQTT integration configured
- Language-specific dependencies (Python packages, Rust toolchain, etc.)
