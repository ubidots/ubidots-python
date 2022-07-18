import pytest
import responses
from responses.matchers import (
    header_matcher,
    json_params_matcher,
    query_param_matcher,
)

import ubidots


@pytest.fixture(autouse=True)
def set_token(mocked_responses):
    TOKEN = "test-token"
    ubidots.token = TOKEN
    ubidots.base_url = "https://industrial.api.ubidots.com"
    ubidots.api_ver = "v2.0"
    ubidots.data_api_ver = "v1.6"
    yield
    for call in mocked_responses.calls:
        assert call.request.headers.items() >= {"X-Auth-Token": TOKEN}.items()


class TestSendDataToDevice:
    def test__send_single_variable_value(self, mocked_responses):
        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device",
            status=200,
            json={"temperature": [{"status_code": 201}]},
            match=[json_params_matcher({"temperature": 10})],
        )

        device = ubidots.Devices.new(label="test-device")
        device.send_data(temperature=10)

    def test__send_multiple_variables_value(self, mocked_responses):
        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device",
            status=200,
            json={
                "temperature": [{"status_code": 201}],
                "humidity": [{"status_code": 201}],
                "pressure": [{"status_code": 201}],
            },
            match=[
                json_params_matcher(
                    {"temperature": 10, "humidity": 90, "pressure": 78}
                )
            ],
        )

        device = ubidots.Devices.new(label="test-device")
        device.send_data(temperature=10, humidity=90, pressure=78)

    def test__send_single_variable_dot(self, mocked_responses):
        dot = {
            "value": 10,
            "timestamp": 1634311791000,
            "context": {"status": "cold"},
        }

        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device",
            status=200,
            json={"temperature": [{"status_code": 201}]},
            match=[json_params_matcher({"temperature": dot})],
        )

        device = ubidots.Devices.new(label="test-device")
        device.send_data(temperature=dot)

    def test__send_multiple_variables_dots(self, mocked_responses):
        temperature = {
            "value": 10,
            "timestamp": 1634311791000,
            "context": {"status": "cold"},
        }
        humidity = {
            "value": 90,
            "timestamp": 1634311791000,
            "context": {"status": "High humidity"},
        }
        pressure = {
            "value": 78,
            "timestamp": 1634311791000,
            "context": {"status": "Normal"},
        }

        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device",
            status=200,
            json={"temperature": [{"status_code": 201}]},
            match=[
                json_params_matcher(
                    {
                        "temperature": temperature,
                        "humidity": humidity,
                        "pressure": pressure,
                    }
                )
            ],
        )

        device = ubidots.Devices.new(label="test-device")
        device.send_data(
            temperature=temperature, humidity=humidity, pressure=pressure
        )

    def test__send_position(self, mocked_responses):
        position = {"value": 1, "context": {"lat": 6.5423, "lng": -70.5783}}

        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device",
            status=200,
            json={"temperature": [{"status_code": 201}]},
            match=[json_params_matcher({"position": position})],
        )

        device = ubidots.Devices.new(label="test-device")
        device.send_data(position=position)


class TestSendDataToVariable:
    def test__send_single_variable_value(self, mocked_responses):
        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device/temperature/values",
            status=200,
            json={"status_code": 201},
            match=[json_params_matcher({"value": 10})],
        )

        device = ubidots.Devices.new(label="test-device")
        variable = device.Variables.new(label="temperature")
        variable.send_data(value=10)

    def test__send_single_variable_dot(self, mocked_responses):
        dot = {
            "value": 10,
            "timestamp": 1634311791000,
            "context": {"status": "cold"},
        }

        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device/temperature/values",
            status=200,
            json={"status_code": 201},
            match=[json_params_matcher(dot)],
        )

        device = ubidots.Devices.new(label="test-device")
        variable = device.Variables.new(label="temperature")
        variable.send_data(**dot)

    def test__send_multiple_variable_dots(self, mocked_responses):
        dots = [
            {
                "value": 10,
                "timestamp": 1634311791000,
                "context": {"status": "cold"},
            },
            {
                "value": 12,
                "timestamp": 1634311891000,
                "context": {"status": "cold"},
            },
            {
                "value": 14,
                "timestamp": 1634311991000,
                "context": {"status": "cold"},
            },
        ]

        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device/temperature/values",
            status=200,
            json=[{"status_code": 201} for _ in enumerate(dots)],
            match=[json_params_matcher(dots)],
        )

        device = ubidots.Devices.new(label="test-device")
        variable = device.Variables.new(label="temperature")
        variable.send_data(*dots)

    def test__send_position(self, mocked_responses):
        position = {"value": 1, "context": {"lat": 6.5423, "lng": -70.5783}}

        mocked_responses.add(
            responses.POST,
            f"https://industrial.api.ubidots.com/api/v1.6/devices/test-device/position/values",
            status=200,
            json={"status_code": 201},
            match=[json_params_matcher(position)],
        )

        device = ubidots.Devices.new(label="test-device")
        variable = device.Variables.new(label="position")
        variable.send_data(**position)
