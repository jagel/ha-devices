#!/usr/bin/env python3
"""
GPIO Utility Library for Series II Wall Push Console Button 34299R
"""

from gpiozero import DigitalOutputDevice
import time


class GenieGarageDevice:
    def __init__(self, giopin: DigitalOutputDevice):
        self.pin = giopin
        self.output_def = "Garage Door Opener"
        self.delay = 2  # seconds
        self.current_state = "OFF"

    def initialize_GPIO(self):
        # Try to initialize GPIO, fallback to simulation if not on Pi
        try:
            from gpiozero import LED
            self.led = LED(self.pin)
            self.SIMULATION_MODE = False
            print("Garage Opener GPIO initialized successfully")
        except Exception as e:
            print(f"Garage Opener GPIO failed: {e}")
            print("Running in SIMULATION MODE - no actual GPIO control")
            self.led = None
            self.SIMULATION_MODE = True        

    def door_up_down(self):
        if self.SIMULATION_MODE:
            print(f"SIMULATION: {self.output_def} event started")
            time.sleep(self.delay)
            print(f"SIMULATION: {self.output_def} event completed")
        else:
            print(f"{self.output_def} event started")
            self.led.on()
            time.sleep(self.delay)
            self.led.off()
            print(f"{self.output_def} event completed")
        self.currentState = "OFF"
