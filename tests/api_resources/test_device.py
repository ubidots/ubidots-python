import json
from datetime import datetime, timezone

import pytest
import responses

import ubidots


@pytest.fixture(autouse=True)
def set_token(mocked_responses):
    TOKEN = "test-token"
    ubidots.config.token = TOKEN
    yield
    for call in mocked_responses.calls:
        assert call.request.headers.items() >= {"X-Auth-Token": TOKEN}.items()


@pytest.mark.parametrize(
    "props",
    [
        {"label": "awesome-device"},
        {"label": "awesome-device", "name": "Awesome Device"},
        {"label": "awesome-device", "description": "Really awesome device!"},
        {"label": "awesome-device", "tags": ["t1", "t2", "t3"]},
        {
            "label": "awesome-device",
            "properties": {"_icon": "awesome-icon", "_color": "#000000"},
        },
        {
            "label": "awesome-device",
            "properties": {
                "_config": {"device-property": {"text": "Device property"}}
            },
        },
    ],
)
def test__create_device(mocked_responses, fake_device, props):
    mocked_responses.add(
        responses.POST,
        f"https://industrial.api.ubidots.com/api/v2.0/devices",
        status=200,
        headers={"Content-Type": "application/json"},
        json=fake_device(**props),
        match=[responses.matchers.json_params_matcher(props)],
    )

    device = ubidots.Device.create(**props)

    for key, val in props.items():
        assert hasattr(device, key)
        assert getattr(device, key) == val


def test__retrieve_device_by_id(mocked_responses, fake_device):
    DEVICE_ID = "0123456789abcdef"
    DEVICE = fake_device(id=DEVICE_ID)
    mocked_responses.add(
        responses.GET,
        f"https://industrial.api.ubidots.com/api/v2.0/devices/{DEVICE_ID}",
        status=200,
        headers={"Content-Type": "application/json"},
        json=DEVICE,
    )

    device = ubidots.Device.retrieve(id=DEVICE_ID)

    for key, val in DEVICE.items():
        assert hasattr(device, key)
        assert getattr(device, key) == val


def test__retrieve_device_by_label(mocked_responses, fake_device):
    DEVICE_LABEL = "awesome-device"
    DEVICE = fake_device(label=DEVICE_LABEL)
    mocked_responses.add(
        responses.GET,
        f"https://industrial.api.ubidots.com/api/v2.0/devices/~{DEVICE_LABEL}",
        status=200,
        headers={"Content-Type": "application/json"},
        json=DEVICE,
    )

    device = ubidots.Device.retrieve(label=DEVICE_LABEL)

    for key, val in DEVICE.items():
        assert hasattr(device, key)
        assert getattr(device, key) == val
