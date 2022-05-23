import json

import pytest
import responses

import ubidots


@pytest.fixture(autouse=True)
def set_token(mocked_responses):
    TOKEN = "test-token"
    ubidots.token = TOKEN
    yield
    for call in mocked_responses.calls:
        assert call.request.headers.items() >= {"X-Auth-Token": TOKEN}.items()
