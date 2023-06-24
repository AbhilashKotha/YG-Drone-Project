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
         patch("server.DroneController.is_drone_armed") as mock_is_drone_armed, \
         patch("server.process_control_request") as mock_process:

        mock_process.return_value = ("success", 200)

        # Test with armed drone
        mock_is_drone_armed.return_value = True
        with client.application.test_request_context(json={"command": "1", "value": 50}):
            result = mock_process("1", 50)
            assert result[1] == 200
            assert result[0] == "success"

        mock_process.return_value = ("error", 400)

        # Test with disarmed drone
        mock_is_drone_armed.return_value = False
        with client.application.test_request_context(json={"command": "1", "value": 50}):
            result = mock_process("1", 50)
            assert result[1] == 400
            assert result[0] == "error"

def test_get_aileron(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_aileron')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "aileron" in data
        assert data["aileron"] == 1500

def test_get_elevator(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_elevator')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "elevator" in data
        assert data["elevator"] == 1500

def test_get_throttle(client, drone_controller):
    drone_controller.get_current_value.return_value = 1000
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_throttle')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "throttle" in data
        assert data["throttle"] == 1000

def test_get_rudder(client, drone_controller):
    drone_controller.get_current_value.return_value = 1500
    with patch("server.DroneController", drone_controller):
        response = client.get('/get_rudder')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "status" in data
        assert data["status"] == "success"
        assert "rudder" in data
        assert data["rudder"] == 1500

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