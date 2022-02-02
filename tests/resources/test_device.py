import json
from datetime import datetime, timezone

import pytest
import responses

import ubidots


@pytest.fixture
def fake_devices(faker):
    def _fake_devices(num_devices=1):
        devices = [
            {
                "url": faker.uri(),
                "id": faker.unique.hexify(text="".join(["^"] * 24)),
                "organization": {
                    "url": faker.uri(),
                    "id": faker.unique.hexify(text="".join(["^"] * 24)),
                    "label": faker.unique.slug(),
                    "name": faker.company(),
                    "createdAt": "@2021-08-03T21:00:28.744343Z",
                },
                "label": faker.unique.slug(),
                "name": faker.words(nb=faker.random_int(min=1, max=4)),
                "description": faker.sentence(nb_words=8),
                "tags": [],
                "properties": {},
                "isActive": True,
                "lastActivity": 0,
                "createdAt": "",
                "variables": faker.uri(),
                "variablesCount": faker.random_int(min=0, max=100),
            }
            for i in range(num_devices)
        ]
        return devices if len(devices) != 1 else devices[0]

    return _fake_devices


def test__retrieve_device(mocked_responses, fake_devices):
    TOKEN = "my-token"
    DEVICE_LABEL = "awesome-device"
    RESPONSE = fake_devices()
    RESPONSE.update({"label": DEVICE_LABEL})
    mocked_responses.add(
        responses.GET,
        f"https://industrial.api.ubidots.com/api/v2.0/devices/~{DEVICE_LABEL}",
        status=200,
        headers={"Content-Type": "application/json"},
        json=RESPONSE,
    )

    ubidots.config.token = TOKEN
    print("ubidots.config.token", id(ubidots.config.token))
    device = ubidots.Device.retrieve(label=DEVICE_LABEL)

    assert "X-Auth-Token" in mocked_responses.calls[0].request.headers
    assert TOKEN == mocked_responses.calls[0].request.headers["X-Auth-Token"]
    assert hasattr(device, "label")
    assert device.label == DEVICE_LABEL


def test__create_device(mocked_responses, fake_devices):
    TOKEN = "my-token"
    DEVICE_LABEL = "awesome-device"
    RESPONSE = fake_devices()
    RESPONSE.update({"label": DEVICE_LABEL})
    mocked_responses.add(
        responses.POST,
        f"https://industrial.api.ubidots.com/api/v2.0/devices",
        status=200,
        headers={"Content-Type": "application/json"},
        json=RESPONSE,
    )

    ubidots.config.token = TOKEN
    device = ubidots.Device.create(label=DEVICE_LABEL)

    assert "X-Auth-Token" in mocked_responses.calls[0].request.headers
    assert TOKEN == mocked_responses.calls[0].request.headers["X-Auth-Token"]
    assert hasattr(device, "label")
    assert device.label == DEVICE_LABEL
