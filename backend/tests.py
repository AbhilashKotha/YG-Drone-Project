import pytest
import json
from server import server, process_control_request
from drone import DroneController
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    server.config['TESTING'] = True
    with server.test_client() as client:
        yield client

@pytest.fixture
def drone_controller():
    controller = MagicMock(spec=DroneController)
    controller.arm_vehicle.return_value = True
    controller.send_rc_command.return_value = True
    controller.vehicle = MagicMock()
    controller.get_current_value.return_value = 1500
    controller.get_altitude.return_value = 100
    controller.get_roll.return_value = 0
    controller.get_pitch.return_value = 0
    controller.get_yaw.return_value = 0
    controller.is_armed = MagicMock()
    yield controller

def test_arm_drone(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.post('/arm_drone')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"

def test_set_aileron(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.post('/set_aileron', json={'set_aileron': 50})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"

def test_set_elevator(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.post('/set_elevator', json={'set_elevator': 50})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"

def test_set_throttle(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.post('/set_throttle', json={'set_throttle': 50})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"

def test_set_rudder(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.post('/set_rudder', json={'set_rudder': 50})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"

def test_process_control_request(client, drone_controller):
    with patch("server.DroneController", return_value=drone_controller), \
         patch("server.is_drone_armed") as mock_is_drone_armed:

        # Test with armed drone
        mock_is_drone_armed.return_value = True
        with client.application.test_request_context(json={"1": 50}):
            result, status_code = process_control_request("1", 50)
            assert status_code == 200
            data = json.loads(result.data)
            assert "status" in data
            assert data["status"] == "success"

        # Test with disarmed drone
        mock_is_drone_armed.return_value = False
        with client.application.test_request_context(json={"1": 50}):
            result, status_code = process_control_request("1", 50)
            assert status_code == 400
            data = json.loads(result.data)
            assert "status" in data
            assert data["status"] == "error"

def test_get_altitude(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_altitude')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "altitude" in data
        assert data["altitude"] == 1500

def test_get_yaw(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_yaw')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "yaw" in data
        assert data["yaw"] == 1500

def test_get_pitch(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_pitch')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "pitch" in data
        assert data["pitch"] == 1500

def test_get_roll(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_roll')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "roll" in data
        assert data["roll"] == 1500

def test_get_altitude_status(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_altitude_status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "altitude_status" in data
        assert data["altitude_status"] == 100

def test_get_roll_status(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_roll_status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "roll_status" in data
        assert data["roll_status"] == 0

def test_get_pitch_status(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_pitch_status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "pitch_status" in data
        assert data["pitch_status"] == 0

def test_get_yaw_status(client, drone_controller):
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_yaw_status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "yaw_status" in data
        assert data["yaw_status"] == 0

def test_disarm_drone(client, drone_controller):
    drone_controller.disarm_vehicle.return_value = True
    with patch("server.DroneController", drone_controller):
        response = client.post('/disarm_drone')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "message" in data
        assert data["message"] == "Drone Disarmed successfully"