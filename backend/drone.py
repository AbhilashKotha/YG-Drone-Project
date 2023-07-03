# Copyright 2023 YG-Drone-Project
"""
Drone or simulator code
"""
import time
from dronekit import connect, VehicleMode

class DroneController:
    """
    Drone controller class
    """
    CONNECTION_STRING = "127.0.0.1:14550"

    def __init__(self):
        """
        Constructor to create the vehicle object
        """
        self.vehicle = connect(self.CONNECTION_STRING, wait_ready=False)
        self.current_values = {1: 1500,
                                2: 1500,
                                  3: 1000,
                                    4: 1500}  # Initialize current values for each channel

    def __del__(self):
        if hasattr(self, 'vehicle'):
            self.vehicle.close()

    #arm vehicle
    def arm_vehicle(self):
        """
        This method is used to arm the vehicle.
        It uses a while loop to ensure that the vehicle is armed.
        """

        self.vehicle.armed = True
        while self.vehicle.armed is False:
            print('Waiting for the drone to arm.')
            time.sleep(1)
        if self.vehicle.armed:
            return True
        return None

    def disarm_vehicle(self):
        """
        This method is used to disarm the vehicle.
        It uses a while loop to ensure that the vehicle is disarmed.
        """

        self.vehicle.armed = False
        while self.vehicle.armed is True:
            print('Waiting for the drone to disarm.')
            time.sleep(1)
        if not self.vehicle.armed:
            return True
        return None

    def send_rc_command(self, control_surface_channel, percent):
        """
        This method is used to modify the control surfaces of the vehicle.
        The control surfaces are the throttle, elevator, rudder, and aileron.
        It changes these controls surfaces by passing a PWM value to the
        specific channel responsible fo r the control surface intended to be
        changed.
        """

        # elevator = '2', throttle = '3', rudder = '4', aileron = '1'
        self.vehicle.mode = VehicleMode("MANUAL")
        self.vehicle.wait_for_mode("MANUAL")
        if self.vehicle.armed: # Check that vehicle is armed before attempting to change the channel
            if control_surface_channel == 3: # Check if the channel is throttle
                pwm=int(1000 + (1000 * percent / 100))
            else:
                # Set the neutral position to 1500 for all others
                pwm = int(1500 + (500 * (percent - 50) / 50))
            self.current_values[control_surface_channel] = pwm
            self.vehicle.channels.overrides = self.current_values
            return True
        return None

    def get_current_value(self, control_surface_channel):
        """
        This function is used to retrieve the current value of a specific control surface channel.
        """
        return self.current_values[control_surface_channel]
