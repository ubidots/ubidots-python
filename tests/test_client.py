from unittest.mock import MagicMock, patch, call

import pytest

from ubidots.client import Ubidots


@pytest.fixture
def api():
    """
    Pytest fixture that provides a Ubidots client with its HttpClient replaced by a mock.
    
    Returns:
        Ubidots: A Ubidots instance whose internal HTTP client (`_http`) is the mocked HttpClient for use in tests.
    """
    with patch("ubidots.client.HttpClient") as MockHttp:
        client = Ubidots("test-token")
        client._http = MockHttp.return_value
        yield client


BASE = "https://industrial.api.ubidots.com"


class TestDevices:
    def test_get_devices_paginates(self, api):
        api._http.get.side_effect = [
            {"results": [{"label": "d1"}], "next": f"{BASE}/api/v2.0/devices/?page=2"},
            {"results": [{"label": "d2"}], "next": None},
        ]
        result = api.get_devices()
        assert result == [{"label": "d1"}, {"label": "d2"}]
        assert api._http.get.call_count == 2

    def test_get_device(self, api):
        api._http.get.return_value = {"label": "my-dev"}
        result = api.get_device("my-dev")
        api._http.get.assert_called_once_with(f"{BASE}/api/v2.0/devices/~my-dev/")
        assert result == {"label": "my-dev"}

    def test_get_device_by_id(self, api):
        api._http.get.return_value = {"id": "abc123"}
        result = api.get_device_by_id("abc123")
        api._http.get.assert_called_once_with(f"{BASE}/api/v2.0/devices/abc123/")
        assert result == {"id": "abc123"}

    def test_create_device(self, api):
        api._http.post.return_value = {"label": "new-dev"}
        result = api.create_device(label="new-dev", name="New Device")
        api._http.post.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/",
            json={"label": "new-dev", "name": "New Device"},
        )
        assert result == {"label": "new-dev"}

    def test_create_device_with_extra_fields(self, api):
        api._http.post.return_value = {}
        api.create_device(label="dev", description="A device")
        api._http.post.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/",
            json={"label": "dev", "description": "A device"},
        )

    def test_update_device(self, api):
        api._http.patch.return_value = {"name": "Updated"}
        result = api.update_device("my-dev", name="Updated")
        api._http.patch.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/~my-dev/",
            json={"name": "Updated"},
        )
        assert result == {"name": "Updated"}

    def test_delete_device(self, api):
        api._http.delete.return_value = None
        api.delete_device("my-dev")
        api._http.delete.assert_called_once_with(f"{BASE}/api/v2.0/devices/~my-dev/")


class TestVariables:
    def test_get_variables_for_device(self, api):
        api._http.get.return_value = {"results": [{"label": "temp"}], "next": None}
        result = api.get_variables("my-dev")
        api._http.get.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/~my-dev/variables/", params={}
        )
        assert result == [{"label": "temp"}]

    def test_get_variables_all(self, api):
        api._http.get.return_value = {"results": [{"label": "temp"}], "next": None}
        result = api.get_variables()
        api._http.get.assert_called_once_with(
            f"{BASE}/api/v2.0/variables/", params={}
        )
        assert result == [{"label": "temp"}]

    def test_get_variable(self, api):
        api._http.get.return_value = {"label": "temp"}
        result = api.get_variable("my-dev", "temp")
        api._http.get.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/~my-dev/variables/~temp/"
        )
        assert result == {"label": "temp"}

    def test_create_variable(self, api):
        api._http.post.return_value = {"label": "temp"}
        result = api.create_variable("my-dev", label="temp", name="Temperature")
        api._http.post.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/~my-dev/variables/",
            json={"label": "temp", "name": "Temperature"},
        )
        assert result == {"label": "temp"}

    def test_update_variable(self, api):
        api._http.patch.return_value = {"name": "Temp Updated"}
        result = api.update_variable("my-dev", "temp", name="Temp Updated")
        api._http.patch.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/~my-dev/variables/~temp/",
            json={"name": "Temp Updated"},
        )
        assert result == {"name": "Temp Updated"}

    def test_delete_variable(self, api):
        api._http.delete.return_value = None
        api.delete_variable("my-dev", "temp")
        api._http.delete.assert_called_once_with(
            f"{BASE}/api/v2.0/devices/~my-dev/variables/~temp/"
        )


class TestDataIngestion:
    def test_send_values(self, api):
        api._http.post.return_value = {"temperature": [{"status_code": 201}]}
        result = api.send_values("my-dev", {"temperature": 22.5, "humidity": 60})
        api._http.post.assert_called_once_with(
            f"{BASE}/api/v1.6/devices/my-dev",
            json={"temperature": 22.5, "humidity": 60},
        )
        assert "temperature" in result

    def test_send_value_simple(self, api):
        api._http.post.return_value = {}
        api.send_value("my-dev", "temp", 22.5)
        api._http.post.assert_called_once_with(
            f"{BASE}/api/v1.6/devices/my-dev/temp/values",
            json={"value": 22.5},
        )

    def test_send_value_dict(self, api):
        api._http.post.return_value = {}
        payload = {"value": 22.5, "timestamp": 1609459200000}
        api.send_value("my-dev", "temp", payload)
        api._http.post.assert_called_once_with(
            f"{BASE}/api/v1.6/devices/my-dev/temp/values",
            json=payload,
        )

    def test_get_values(self, api):
        api._http.get.return_value = [{"value": 22.5}]
        result = api.get_values("my-dev", "temp", page_size=10)
        api._http.get.assert_called_once_with(
            f"{BASE}/api/v1.6/devices/my-dev/temp/values",
            params={"page_size": 10},
        )
        assert result == [{"value": 22.5}]

    def test_get_last_value(self, api):
        api._http.get.return_value = 22.5
        result = api.get_last_value("my-dev", "temp")
        api._http.get.assert_called_once_with(
            f"{BASE}/api/v1.6/devices/my-dev/temp/lv"
        )
        assert result == 22.5


class TestPagination:
    def test_paginate_single_page(self, api):
        api._http.get.return_value = {
            "results": [{"id": 1}, {"id": 2}],
            "next": None,
        }
        result = api._paginate("http://example.com/api", {})
        assert result == [{"id": 1}, {"id": 2}]

    def test_paginate_multiple_pages(self, api):
        api._http.get.side_effect = [
            {"results": [{"id": 1}], "next": "http://example.com/api?page=2"},
            {"results": [{"id": 2}], "next": "http://example.com/api?page=3"},
            {"results": [{"id": 3}], "next": None},
        ]
        result = api._paginate("http://example.com/api", {"size": 1})
        assert result == [{"id": 1}, {"id": 2}, {"id": 3}]
        # First call includes params, subsequent calls don't (next URL has them)
        calls = api._http.get.call_args_list
        assert calls[0] == call("http://example.com/api", params={"size": 1})
        assert calls[1] == call("http://example.com/api?page=2", params={})


class TestCustomBaseUrl:
    def test_custom_base_url(self):
        with patch("ubidots.client.HttpClient"):
            api = Ubidots("tok", base_url="https://custom.example.com")
        assert api._endpoints.base_url == "https://custom.example.com"
