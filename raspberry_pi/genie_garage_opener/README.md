# Device Name Template



Environment 

```bash
python3 -m venv ~/genie_garage_opener
```
```bash
source ~/genie_garage_opener/bin/activate
```

## Description
Garage opener device. Compatible with Genie Series II Wall Push Console Button 34299R

## Hardware Requirements

Example:
- 1x Raspberry Pi 5
- 1x Relay module 1 channel

## Wiring Diagram

```
Raspberry Pi    
------------    -----
5V         -->  VCC
GND        -->  GND
GPIO 7     -->  RELAY IN
```

![Alt text](./docs/diagram.png)


## Software Dependencies

### Python
Create a `requirements.txt` file:
```
paho-mqtt>=1.6.0
python
```


## Installation

### 1. Hardware Setup
Step-by-step instructions for connecting components to the Raspberry Pi.

### 2. Create .env file

```
# .env
mqtt_broker=<your-mqtt_broker>
mqtt_username=<your-mqtt_username>
mqtt_password=<your-mqtt_password>
```

### 2. Software Setup (Python)
```bash
# Clone or copy this directory to your Raspberry Pi
cd raspberry_pi/genie_garage_opener

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure settings
# cp config.example.yaml config.yaml
# Edit config.yaml with your settings

# Run the device
python3 main.py
```

### 3. Run as Service (Optional)
Create a systemd service to run on boot:

```bash
sudo nano /etc/systemd/system/ha-device.service
```

```ini
[Unit]
Description=Home Assistant Device
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ha-devices/raspberry_pi/device_name
ExecStart=/home/pi/ha-devices/raspberry_pi/device_name/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable ha-device.service
sudo systemctl start ha-device.service
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

Create a `config.yaml` file:
```yaml
mqtt:
  broker: "192.168.1.100"
  port: 1883
  username: "mqtt_user"
  password: "mqtt_password"
  
device:
  name: "Living Room Sensor"
  unique_id: "device_name_001"
  update_interval: 60  # seconds
  
gpio:
  data_pin: 4  # GPIO pin number
```

## Troubleshooting

### Device won't start
- Check Python version (3.7+)
- Verify all dependencies installed
- Check file permissions

### Device won't connect to MQTT
- Verify broker IP address and port
- Check MQTT credentials
- Ensure broker is running and accessible

### No data in Home Assistant
- Check MQTT topics in MQTT explorer
- Verify discovery is enabled
- Check device logs: `journalctl -u ha-device.service -f`

### Permission Errors with GPIO
```bash
sudo usermod -a -G gpio pi
# Log out and back in
```

## License
MIT License (inherited from repository)



## Run application 

Execute the following command
```bash
nohup python3 /home/jagel/Documents/repos/ha-devices/raspberry_pi/genie_garage_opener/src/main.py > /dev/null 2>&1 &
```

This will:

- Run the process in the background (&)
- Ignore hangup signals (nohup)
- Redirect output to null to avoid log files
- Continue running even after you close the terminal

To check if it's running:

```bash
ps aux | grep main.py
```

To stop the application run the command

```bash
pkill -f main.py
```
