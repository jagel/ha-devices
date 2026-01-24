#!/usr/bin/env python3
"""
Home assitant and MQTT Configuration
"""

import os
import json
from pyaml_env import parse_config
from dotenv import load_dotenv

class YamlConfigLoader:
    """
    Load configuration from YAML file
    """
    def __init__(self, config_file='./config.yaml'):
        self.config_file = config_file
        self.config = None
        # Load environment variables from .env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)

    def load_config(self):
        """
        Load configuration from YAML file
        
        Args:
            config_file (str): Name of the config file (defaults to 'config.yaml')
        
        Returns:
            dict: Loaded configuration
        """
        if self.config is None:
            config_path = os.path.join(os.path.dirname(__file__), self.config_file)
            try:
                print(f"Loading config from: {config_path}")
                # parse_config expects a file path, not a file object
                self.config = parse_config(config_path)
                print("Config loaded successfully")
            except FileNotFoundError:
                print(f"Config file not found: {config_path}")
                raise
            except Exception as e:
                print(f"Error parsing YAML config: {e}")
                raise
        return self.config

    def get_value(self, nodename, fieldname):
        """
        Get configuration value by nodename and fieldname
        
        Args:
            nodename (str): The top-level node name (e.g., 'mqtt', 'device', 'gpio')
            fieldname (str): The field name within the node (e.g., 'broker', 'username', 'pin')
        
        Returns:
            The configuration value if found, None if not found
        """
        try:
            config = self.load_config()
            return config[nodename][fieldname]
        except KeyError as e:
            print(f"Configuration key not found: {e}")
            return None    

# Global config variable to store loaded configuration

class HA_MQTT_Config:
    def __init__(self, device_id: str, version: str):
        """
        Initialize HA MQTT configuration
        Args:
            device_id (str): Unique device identifier
            version (str): Device version
        """
        self.device_id = device_id
        self.device_name = "Genie Garage Opener"
        self.version = version
        self.unique_identifier = f"ggo_v{self.version}"
        self.command_topic = f"homeassistant/switch/{self.device_id}/set"
        self.state_topic = f"homeassistant/switch/{self.device_id}/state"
        self.discovery_topic = f"homeassistant/switch/{self.device_id}/config"

    def get_discovery_payload(self):
        """Generate Home Assistant MQTT Discovery configuration payload"""
        discovery_payload = {
            "name": self.device_name,
            "unique_id": self.device_id,
            "command_topic": self.command_topic,
            "state_topic": self.state_topic,
            "payload_on": "ON",
            "payload_off": "OFF",
            "state_on": "ON",
            "state_off": "OFF",
            "device_class": "switch",
            "platform": "button",
            "device": {
                "identifiers": [self.unique_identifier],
                "name": self.device_name,
                "model": self.unique_identifier,
                "manufacturer": "Jagel"
            }
        }
        return json.dumps(discovery_payload)

class Device_Config:
    """
    Load MQTT configuration from JSON file
    """
    def __init__(self, config_file: YamlConfigLoader):
        self.config_file = config_file
        #mqtt
        self.broker = self.config_file.get_value('mqtt','broker') 
        self.username = self.config_file.get_value('mqtt','username')
        self.password = self.config_file.get_value('mqtt','password')
        self.port = self.config_file.get_value('mqtt','port')
        self.keepalive = self.config_file.get_value('mqtt','keepalive')
        # device
        self.version = self.config_file.get_value('device','version')
        self.id = self.config_file.get_value('device','id')
        # gpio
        self.garage_door_pin = self.config_file.get_value('gpio','garage_door_pin')
            


class JGL_MQTT:
    """
    MQTT Configuration Loader
    """
    def __init__(self, config_file='config.json'):
        self.config_loader = YamlConfigLoader(config_file)
        self.config = self.config_loader.load_config()
        
    def get_value(self, nodename, fieldname):
        """
        Get configuration value by nodename and fieldname
        
        Args:
            nodename (str): The top-level node name (e.g., 'mqtt', 'device', 'gpio')
            fieldname (str): The field name within the node (e.g., 'broker', 'username', 'pin')
        
        Returns:
            The configuration value if found, None if not found
        """
        try:
            return self.config[nodename][fieldname]
        except KeyError as e:
            print(f"Configuration key not found: {e}")
            return None