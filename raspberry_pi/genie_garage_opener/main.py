#!/usr/bin/env python3
"""
MQTT Garage opener
"""

import paho.mqtt.client as mqtt
from genie_wall_console_lib import GenieGarageDevice
from ha_mqqt_setup_lib import HA_MQTT_Config, JsonConfigLoader, JsonConfig

# Configuration
config = JsonConfigLoader()
device = JsonConfig(config)

# Initialization
genie_garage = GenieGarageDevice(device.garage_door_pin)
genie_garage.initialize_GPIO()

ha_mqtt = HA_MQTT_Config(device.id,device.version)

def on_connect(client, userdata, flags, rc):
    """Callback for when client connects to MQTT broker"""
    if rc == 0:
        print("Connected to MQTT broker successfully")
        client.subscribe(ha_mqtt.command_topic)
        publish_discovery()
        # Publish initial state
        publish_state()
    else:
        print(f"on_connect : Failed to connect to MQTT broker: {rc}")

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages"""
    
    try:
        payload = msg.payload.decode()
        print(f"Received command: {payload}")
        genie_garage.door_up_down()
        publish_state()
            
    except Exception as e:
        print(f"on_message : Error processing message: {e}")

def publish_state():
    """Publish current switch state to Home Assistant"""
    client.publish(ha_mqtt.state_topic, genie_garage.current_state, retain=True)
    print(f"Published state: {genie_garage.current_state}")

def publish_discovery():
    """Publish Home Assistant MQTT Discovery configuration"""
    discovery_payload = ha_mqtt.get_discovery_payload()
    
    client.publish(ha_mqtt.discovery_topic, discovery_payload, retain=True)
    print(f"Published discovery config to: {ha_mqtt.discovery_topic}")

def main():
    """Main function"""
    global client
    
    # Create MQTT client
    client = mqtt.Client()
    client.username_pw_set(device.username,device.password)
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Connect to broker
    try:
        print(f"Connecting to MQTT broker {device.broker}:{device.port}")
        client.connect(device.broker, device.port, device.keepalive)
        print(f"Listening for commands on: {ha_mqtt.command_topic}")
        print(f"Publishing state to: {ha_mqtt.state_topic}")
        
        # Start the loop
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        client.disconnect()
    except Exception as e:
        client.disconnect()
        print(f"Error __main__: {e}")

if __name__ == "__main__":
    main()