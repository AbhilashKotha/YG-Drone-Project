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
    return jsonify({"status": "success", "throttle": DroneController.get_current_value(3)}), 200

@server.route('/get_yaw', methods=['GET'])
def get_yaw():
    return jsonify({"status": "success", "yaw": DroneController.get_current_value(4)}), 200

@server.route('/get_pitch', methods=['GET'])
def get_pitch():
    return jsonify({"status": "success", "pitch": DroneController.get_current_value(2)}), 200

@server.route('/get_roll', methods=['GET'])
def get_roll():
    return jsonify({"status": "success", "roll": DroneController.get_current_value(1)}), 200


@server.route('/arm_drone', methods=['POST'])
def arm_drone():
    try:
        print("Arming drone...")
        result = DroneController.arm_vehicle()
        print("Drone armed successfully.")
        return jsonify({"status": "success", "message": "Drone armed successfully"}), 200
    except Exception as e:
        print(f"Error arming drone: {str(e)}")
        return jsonify({"status": "error", "message": f"Error arming drone: {str(e)}"}), 500

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

    # Updated line: Check if the percent value is within the allowed range (0 to 100).
    # If it's not, set it to the nearest limit (0 or 100).
    percent = min(max(percent, 0), 100)

    return send_rc_command(channel, percent)


def send_rc_command(control_surface_channel, percent):
    try:
        print(f"Setting control surface channel {control_surface_channel} to {percent}%...")
        DroneController.send_rc_command(control_surface_channel, percent)
        print("Control surface channel set successfully.")

        return jsonify({"status": "success", "message": "Control surface channel set successfully"}), 200
    except ValueError as ve:
        print(f"Value error: {str(ve)}")
        return jsonify({"status": "error", "message": f"Value error: {str(ve)}"}), 400
    except Exception as e:
        print(f"Error setting control surface channel: {str(e)}")
        return jsonify({"status": "error", "message": f"Error setting control surface channel: {str(e)}"}), 500

if __name__ == '__main__':
    DroneController = DroneController()
    server.run(port=8000, host='0.0.0.0', debug=True)