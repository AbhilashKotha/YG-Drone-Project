# drone.py
# Copyright 2023 YG-Drone-Project

# Necessary imports
from dronekit import connect, VehicleMode
import time

class DroneController:
    CONNECTION_STRING = "127.0.0.1:14550"

    def __init__(self):
        """
        Constructor to create the vehicle object by connecting to it.
        Also, initializes current PWM values for each control channel.
        """
        self.vehicle = connect(self.CONNECTION_STRING, wait_ready=False)
        self.current_values = {1: 1500, 2: 1500, 3: 1000, 4: 1500}  # Initialize current values for each channel

    def __del__(self):
        """
        Destructor to ensure the vehicle connection is closed when the DroneController object is deleted.
        """
        if hasattr(self, 'vehicle'):
            self.vehicle.close()
    
    def arm_vehicle(self):
        """
        Arms the vehicle. This process might take a moment, so a loop
        checks the vehicle's status until it's confirmed to be armed.
        """

        self.vehicle.armed = True
        while self.vehicle.armed==False:
            print('Waiting for the drone to arm.')
            time.sleep(1)
        if self.vehicle.armed:
            return True
        
    def disarm_vehicle(self):
        """
        Disarms the vehicle. Again, the process is checked in a loop
        until the vehicle's status confirms it has disarmed.
        """

        self.vehicle.armed = False
        while self.vehicle.armed==True:
            print('Waiting for the drone to disarm.')
            time.sleep(1)
        if not self.vehicle.armed:
            return True

    def send_rc_command(self, control_surface_channel, percent):
        """
        Sends command to modify the control surfaces (throttle, elevator, rudder, aileron)
        via the appropriate channel using a PWM value calculated from a percent input.
        """

        # elevator = '2', throttle = '3', rudder = '4', aileron = '1'
        self.vehicle.mode = VehicleMode("MANUAL")
        self.vehicle.wait_for_mode("MANUAL")
        if self.vehicle.armed: # Check that vehicle is armed before attempting to change the channel
            if control_surface_channel == 3: # Check if the channel is throttle 
                pwm=int(1000 + (1000 * percent / 100))
            else:
                pwm = int(1500 + (500 * (percent - 50) / 50)) # Set the neutral position to 1500 for all others
            
            self.current_values[control_surface_channel] = pwm
            self.vehicle.channels.overrides = self.current_values
            return True
        
    def get_current_value(self, control_surface_channel):
        """
        Retrieves the current PWM value of a specified control surface channel.
        """
        return self.current_values[control_surface_channel]
    
    def get_altitude(self):
        """
        Retrieves the altitude of the vehicle.
        """
        return self.vehicle.location.global_relative_frame.alt
    
    def get_roll(self):
        """
        Retrieves the roll attitude of the vehicle.
        """
        return self.vehicle.attitude.roll

    def get_pitch(self):
        """
        Retrieves the pitch attitude of the vehicle.
        """
        return self.vehicle.attitude.pitch

    def get_yaw(self):
        """
        Retrieves the yaw attitude of the vehicle.
        """
        return self.vehicle.attitude.yaw