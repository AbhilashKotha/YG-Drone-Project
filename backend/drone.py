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
        self.flight_path = []

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

        self.vehicle.armed = False
        while self.vehicle.armed==True:
            print('Waiting for the drone to disarm.')
            time.sleep(1)
        if not self.vehicle.armed:
            # Save the flight path to a file
            self.save_flight_path()
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
            self.vehicle.add_attribute_listener('global_frame', self.log_coordinates)
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

    def save_flight_path(self):
        """
        Save the flight path to a file
        """
        with open('flight_path.txt', 'w') as f:
            for coordinate in self.flight_path:
                f.write("Latitude: {}, Longitude: {}, Altitude: {}\n".format(
                    coordinate.lat, coordinate.lon, coordinate.alt))