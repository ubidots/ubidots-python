from urllib.parse import urljoin

import pytest

from ubidots.api_client import _api_url


@pytest.fixture
def fake_id(faker):
    def _fake_id():
        return faker.unique.hexify(text="".join(["^"] * 24))

    return _fake_id


@pytest.fixture
def fake_device(faker, fake_id):
    def _fake_device(fields: list = [], **props):
        device_id = fake_id()
        device = {
            "url": urljoin(_api_url, f"devices/{device_id}"),
            "id": device_id,
            "organization": None,
            "label": faker.unique.slug(),
            "name": " ".join(faker.words(nb=faker.random_int(min=0, max=4))),
            "description": faker.sentence(
                nb_words=faker.random_int(min=0, max=8)
            ),
            "tags": [],
            "properties": {},
            "isActive": True,
            "lastActivity": 0,
            "createdAt": "",
            "variables": urljoin(_api_url, f"devices/{device_id}/variables"),
            "variablesCount": 0,
        }
        for key, val in props.items():
            device[key] = val
        return {k: v for k, v in device.items() if not fields or k in fields}

    return _fake_device


@pytest.fixture
def fake_devices(faker, fake_device):
    def _fake_devices(count: int = 1, fields: list = [], props: list = []):
        props_it = iter(props)
        return [fake_device(fields, **next(props_it, {})) for _ in range(count)]

    return _fake_devices
