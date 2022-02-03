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


def test__retrieve_device(mocked_responses, fake_device):
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

    assert hasattr(device, "label")
    assert device.label == DEVICE_LABEL


def test__create_device(mocked_responses, fake_device):
    DEVICE_LABEL = "awesome-device"
    DEVICE = fake_device(label=DEVICE_LABEL)
    mocked_responses.add(
        responses.POST,
        f"https://industrial.api.ubidots.com/api/v2.0/devices",
        status=200,
        headers={"Content-Type": "application/json"},
        json=DEVICE,
    )

    device = ubidots.Device.create(label=DEVICE_LABEL)

    assert hasattr(device, "label")
    assert device.label == DEVICE_LABEL
