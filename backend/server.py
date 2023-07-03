# Copyright 2023 YG-Drone-Project
"""
Flask component which acts as a middle layer between UI and the Simulator code.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from drone import DroneController

server = Flask(__name__)
CORS(server)

def is_drone_armed():
    """
    Checks to make sure that the drone is armed before allowing
    a user to change the control surfaces
    """

    return DroneController.vehicle.armed

@server.route('/get_throttle', methods=['GET'])
def get_throttle():
    """
    Get throttle value
    """
    return jsonify({"status": "success", "throttle": DroneController.get_current_value(3)}), 200

@server.route('/get_yaw', methods=['GET'])
def get_yaw():
    """
    Get yaw value
    """
    return jsonify({"status": "success", "yaw": DroneController.get_current_value(4)}), 200

@server.route('/get_pitch', methods=['GET'])
def get_pitch():
    """
    Get pitch value
    """
    return jsonify({"status": "success", "pitch": DroneController.get_current_value(2)}), 200

@server.route('/get_roll', methods=['GET'])
def get_roll():
    """
    Get roll value
    """
    return jsonify({"status": "success", "roll": DroneController.get_current_value(1)}), 200


@server.route('/arm_drone', methods=['POST'])
def arm_drone():
    """
    arm the drone
    """
    try:
        print("Arming drone...")
        DroneController.arm_vehicle()
        print("Drone armed successfully.")
        return jsonify({"status": "success", "message": "Drone armed successfully"}), 200
    except Exception as ex_arm:
        print(f"Error arming drone: {str(ex_arm)}")
        return jsonify({"status": "error", "message": f"Error arming drone: {str(ex_arm)}"}), 500

@server.route('/disarm_drone', methods=['POST'])
def disarm_drone():
    """
    disarm the drone
    """
    try:
        print("Disarming drone...")
        DroneController.disarm_vehicle()
        print("Drone Disarmed successfully.")
        return jsonify({"status": "success",
                        "message": "Drone Disarmed successfully"}), 200
    except Exception as ex_disarm:
        print(f"Error Disarming drone: {str(ex_disarm)}")
        return jsonify({"status": "error",
                        "message": f"Error Disarming drone: {str(ex_disarm)}"}), 500


@server.route('/set_aileron', methods=['POST'])
def set_aileron():
    """
    set an aileron value
    """

    return process_control_request('set_aileron', 1)

@server.route('/set_elevator', methods=['POST'])
def set_elevator():
    """
    Set elevator value
    """

    return process_control_request('set_elevator', 2)

@server.route('/set_throttle', methods=['POST'])
def set_throttle():
    """
    set throttle value
    """
    return process_control_request('set_throttle', 3)

@server.route('/set_rudder', methods=['POST'])
def set_rudder():
    """
    set rudder value
    """

    return process_control_request('set_rudder', 4)

def process_control_request(control_surface, channel):
    """
    This function is meant to enforce security checks on surface control
    inputs coming from the user. It checks to ensure that the drone is
    armed and that the control values in percent are within the allowed range.
    """

    if not is_drone_armed():
        return jsonify({"status": "error",
                         "message": "Drone is not armed yet!"}), 400

    percent = request.json[control_surface]

    if not 0 <= percent <= 100:
        return jsonify({"status": "error",
                         "message": "Percent value should be between 0 and 100"}), 400

    return send_rc_command(channel, percent)

def send_rc_command(control_surface_channel, percent):
    """
    send an RC command to the drone
    """
    try:
        print(f"Setting control surface channel {control_surface_channel} to {percent}%...")
        DroneController.send_rc_command(control_surface_channel, percent)
        print("Control surface channel set successfully.")

        return jsonify({"status": "success",
                         "message": "Control surface channel set successfully"}), 200
    except ValueError as val_er:
        print(f"Value error: {str(val_er)}")
        return jsonify({"status": "error", "message": f"Value error: {str(val_er)}"}), 400
    except Exception as exception:
        print(f"Error setting control surface channel: {str(exception)}")
        return jsonify({"status": "error",
                         "message": f"Error setting control surface channel: {str(exception)}"}),500

if __name__ == '__main__':
    DroneController = DroneController()
    server.run(port=8000, host='0.0.0.0', debug=True)
