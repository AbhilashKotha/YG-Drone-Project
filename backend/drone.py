# Copyright 2023 YG-Drone-Project

from dronekit import connect, VehicleMode
import time

class DroneController:
    CONNECTION_STRING = "127.0.0.1:14550"

    def __init__(self):
        """
        Constructor to create the vehicle object
        """
        self.vehicle = connect(self.CONNECTION_STRING, wait_ready=False)
        self.current_values = {1: 1500, 2: 1500, 3: 1000, 4: 1500}  # Initialize current values for each channel

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
        while self.vehicle.armed==False:
            print('Waiting for the drone to arm.')
            time.sleep(1)
        if self.vehicle.armed:
            return True
        
    def disarm_vehicle(self):
        """
        This method is used to disarm the vehicle.
        It uses a while loop to ensure that the vehicle is disarmed.
        """
        if self.vehicle.groundspeed > 0.1:
            print("The vehicle is still moving. Wait for it to come to a complete stop before disarming.")
            return

        if self.vehicle.airspeed > 0.1:
            print("The vehicle is still experiencing airspeed. Wait for it to reduce to zero before disarming.")
            return

        if self.vehicle.location.global_relative_frame.alt > 0.2:
            print("The vehicle is not close enough to the ground. Descend to a lower altitude before disarming.")
            return

        self.vehicle.armed = False
        while self.vehicle.armed==True:
            print('Waiting for the drone to disarm.')
            time.sleep(1)
        if not self.vehicle.armed:
            return True

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
                pwm = int(1500 + (500 * (percent - 50) / 50)) # Set the neutral position to 1500 for all others
            
            self.current_values[control_surface_channel] = pwm
            self.vehicle.channels.overrides = self.current_values
            return True
        
    def get_current_value(self, control_surface_channel):
        """
        This function is used to retrieve the current value of a specific control surface channel.
        """
        return self.current_values[control_surface_channel]