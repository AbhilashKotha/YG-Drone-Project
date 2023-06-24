# Copyright 2023 YG-Drone-Project
import logging
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dronekit import connect, VehicleMode
import time

# set up logging
logging.basicConfig(level=logging.INFO)

server = Flask(__name__)
CORS(server)

# Initialize the DroneController here
DroneController = None

class DroneController:
    # Make the CONNECTION_STRING configurable
    CONNECTION_STRING = os.getenv('DRONE_CONNECTION_STRING', '127.0.0.1:14550')

    def __init__(self):
        """
        Constructor to create the vehicle object
        """
        self.vehicle = connect(self.CONNECTION_STRING, wait_ready=False)
        self.current_values = {1: 1500, 2: 1500, 3: 1000, 4: 1500}  # Initialize current values for each channel

    def __del__(self):
        if hasattr(self, 'vehicle'):
            self.vehicle.close()

    # arm vehicle
    def arm_vehicle(self):
        """
        This method is used to arm the vehicle.
        It uses a while loop to ensure that the vehicle is armed.
        """

        self.vehicle.armed = True
        while self.vehicle.armed == False:
            logging.info('Waiting for the drone to arm.')
            time.sleep(1)
        if self.vehicle.armed:
            return True

    def disarm_vehicle(self):
        """
        This method is used to disarm the vehicle.
        It uses a while loop to ensure that the vehicle is disarmed.
        """

        self.vehicle.armed = False
        while self.vehicle.armed == True:
            logging.info('Waiting for the drone to disarm.')
            time.sleep(1)
        if not self.vehicle.armed:
            return True

    def send_rc_command(self, control_surface_channel, percent):
        """
        This method is used to modify the control surfaces of the vehicle.
        The control surfaces are the throttle, elevator, rudder, and aileron.
        It changes these controls surfaces by passing a PWM value to the
        specific channel responsible for the control surface intended to be
        changed.
        """

        # elevator = '2', throttle = '3', rudder = '4', aileron = '1'
        self.vehicle.mode = VehicleMode("MANUAL")
        self.vehicle.wait_for_mode("MANUAL")
        if self.vehicle.armed:  # Check that vehicle is armed before attempting to change the channel
            if control_surface_channel == 3:  # Check if the channel is throttle
                pwm = int(1000 + (1000 * percent / 100))
            else:
                pwm = int(1500 + (500 * (percent - 50) / 50))  # Set the neutral position to 1500 for all others

            self.current_values[control_surface_channel] = pwm
            self.vehicle.channels.overrides = self.current_values
            return True

    def get_current_value(self, control_surface_channel):
        """
        This function is used to retrieve the current value of a specific control surface channel.
        """
        return self.current_values[control_surface_channel]


def is_drone_armed():
    """
    Checks to make sure that the drone is armed before allowing
    a user to change the control surfaces
    """
    return DroneController.vehicle.armed


@server.route('/get_throttle', methods=['GET'])
def get_throttle():
    return jsonify({"status": "success", "throttle": DroneController.get_current_value(3)}), 200

@server.route('/get_rudder', methods=['GET'])
def get_rudder():
    return jsonify({"status": "success", "rudder": DroneController.get_current_value(4)}), 200

@server.route('/get_elevator', methods=['GET'])
def get_elevator():
    return jsonify({"status": "success", "elevator": DroneController.get_current_value(2)}), 200

@server.route('/get_aileron', methods=['GET'])
def get_aileron():
    return jsonify({"status": "success", "aileron": DroneController.get_current_value(1)}), 200

@server.route('/arm_drone', methods=['POST'])
def arm_drone():
    try:
        logging.info("Arming drone...")
        result = DroneController.arm_vehicle()
        logging.info("Drone armed successfully.")
        return jsonify({"status": "success", "message": "Drone armed successfully"}), 200
    except Exception as e:
        logging.error(f"Error arming drone: {str(e)}")
        return jsonify({"status": "error", "message": f"Error arming drone: {str(e)}"}), 500

@server.route('/disarm_drone', methods=['POST'])
def disarm_drone():
    try:
        logging.info("Disarming drone...")
        result = DroneController.disarm_vehicle()
        logging.info("Drone Disarmed successfully.")
        return jsonify({"status": "success", "message": "Drone Disarmed successfully"}), 200
    except Exception as e:
        logging.error(f"Error Disarming drone: {str(e)}")
        return jsonify({"status": "error", "message": f"Error Disarming drone: {str(e)}"}), 500

@server.route('/set_aileron', methods=['POST'])
def set_aileron():
    return process_control_request('set_aileron', 1)

@server.route('/set_elevator', methods=['POST'])
def set_elevator():
    return process_control_request('set_elevator', 2)

@server.route('/set_throttle', methods=['POST'])
def set_throttle():
    return process_control_request('set_throttle', 3)

@server.route('/set_rudder', methods=['POST'])
def set_rudder():
    return process_control_request('set_rudder', 4)

def process_control_request(control_surface, channel):
    """
    This function is meant to enforce security checks on surface control
    inputs coming from the user. It checks to ensure that the drone is
    armed and that the control values in percent are within the allowed range.
    """
    if not is_drone_armed():
        return jsonify({"status": "error", "message": "Drone is not armed! Arm the drone before attempting to fly."}), 400

    percent = request.json[control_surface]
    if control_surface not in ['set_aileron', 'set_elevator', 'set_throttle', 'set_rudder']:
        return jsonify({"status": "error", "message": "Invalid control surface"}), 400

    if not (0 <= percent <= 100):
        return jsonify({"status": "error", "message": "Percent value should be between 0 and 100"}), 400

    return send_rc_command(channel, percent)

def send_rc_command(control_surface_channel, percent):
    try:
        logging.info(f"Setting control surface channel {control_surface_channel} to {percent}%...")
        DroneController.send_rc_command(control_surface_channel, percent)
        logging.info("Control surface channel set successfully.")

        return jsonify({"status": "success", "message": "Control surface channel set successfully"}), 200
    except ValueError as ve:
        logging.error(f"Value error: {str(ve)}")
        return jsonify({"status": "error", "message": f"Value error: {str(ve)}"}), 400
    except Exception as e:
        logging.error(f"Error setting control surface channel: {str(e)}")
        return jsonify({"status": "error", "message": f"Error setting control surface channel: {str(e)}"}), 500

if __name__ == '__main__':
    DroneController = DroneController()
    server.run(port=os.getenv('PORT', 8000), host='0.0.0.0', debug=os.getenv('DEBUG', True))
