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