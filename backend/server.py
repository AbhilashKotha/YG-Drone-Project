# server.py
# Copyright 2023 YG-Drone-Project

from flask import Flask, request, jsonify
from flask_cors import CORS
from drone import DroneController
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Flask(__name__)
CORS(server)

def is_drone_armed():
    """
    Verifies if the drone is armed before permitting changes
    to control surfaces by users.
    """
    return DroneController.vehicle.armed

@server.route('/get_altitude', methods=['GET'])
def get_altitude():
    return jsonify({"status": "success", "altitude": DroneController.get_current_value(4)}), 200

@server.route('/get_yaw', methods=['GET'])
def get_yaw():
    return jsonify({"status": "success", "yaw": DroneController.get_current_value(3)}), 200

@server.route('/get_pitch', methods=['GET'])
def get_pitch():
    return jsonify({"status": "success", "pitch": DroneController.get_current_value(2)}), 200

@server.route('/get_roll', methods=['GET'])
def get_roll():
    return jsonify({"status": "success", "roll": DroneController.get_current_value(1)}), 200

@server.route('/arm_drone', methods=['POST'])
def arm_drone():
    try:
        logger.info("Arming drone...")
        result = DroneController.arm_vehicle()
        logger.info("Drone armed successfully.")
        return jsonify({"status": "success", "message": "Drone armed successfully"}), 200
    except Exception as e:
        logger.error(f"Error arming drone: {str(e)}")
        return jsonify({"status": "error", "message": f"Error arming drone: {str(e)}"}), 500

@server.route('/disarm_drone', methods=['POST'])
def disarm_drone():
    try:
        logger.info("Disarming drone...")
        result = DroneController.disarm_vehicle()
        logger.info("Drone Disarmed successfully.")
        return jsonify({"status": "success", "message": "Drone Disarmed successfully"}), 200
    except Exception as e:
        logger.error(f"Error Disarming drone: {str(e)}")
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

@server.route('/get_current_value_status', methods=['GET'])
def get_current_value_status():
    return jsonify({"status": "success", "current_value_status": DroneController().get_current_values()}), 200

@server.route('/get_altitude_status', methods=['GET'])
def get_altitude_status():
    return jsonify({"status": "success", "altitude_status": DroneController.get_altitude()}), 200

@server.route('/get_roll_status', methods=['GET'])
def get_roll_status():
    return jsonify({"status": "success", "roll_status": DroneController.get_roll()}), 200

@server.route('/get_pitch_status', methods=['GET'])
def get_pitch_status():
    return jsonify({"status": "success", "pitch_status": DroneController.get_pitch()}), 200

@server.route('/get_yaw_status', methods=['GET'])
def get_yaw_status():
    return jsonify({"status": "success", "yaw_status": DroneController.get_yaw()}), 200

def process_control_request(control_surface, channel):
    """
    This function is meant to enforce security checks on surface control
    inputs coming from the user. It checks to ensure that the drone is
    armed and that the control values in percent are within the allowed range.
    """
    if not is_drone_armed():
        return jsonify({"status": "error", "message": "Drone is not armed! Arm the drone before attempting to fly."}), 400

    percent = request.json[control_surface]

    if not (0 <= percent <= 100):
        return jsonify({"status": "error", "message": "Percent value should be between 0 and 100"}), 400

    return send_rc_command(channel, percent)

def send_rc_command(control_surface_channel, percent):
    try:
        logger.info(f"Setting control surface channel {control_surface_channel} to {percent}%...")
        DroneController.send_rc_command(control_surface_channel, percent)
        logger.info("Control surface channel set successfully.")
        return jsonify({"status": "success", "message": "Control surface channel set successfully"}), 200
    except ValueError as ve:
        logger.error(f"Value error: {str(ve)}")
        return jsonify({"status": "error", "message": f"Value error: {str(ve)}"}), 400
    except Exception as e:
        logger.error(f"Error setting control surface channel: {str(e)}")
        return jsonify({"status": "error", "message": f"Error setting control surface channel: {str(e)}"}), 500

if __name__ == '__main__':
    DroneController = DroneController()
    server.run(port=8000, host='0.0.0.0', debug=False)
