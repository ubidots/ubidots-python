from unittest.mock import MagicMock, patch

import pytest

from ubidots._http import HttpClient
from ubidots.exceptions import (
    UbidotsError400,
    UbidotsError404,
    UbidotsError500,
    UbidotsForbiddenError,
    UbidotsHTTPError,
)


@pytest.fixture
def http():
    """
    Provide a configured HttpClient instance for tests.
    
    Returns:
        HttpClient: an HttpClient initialized with the token "test-token".
    """
    return HttpClient("test-token")


class TestHttpClientInit:
    def test_sets_auth_header(self, http):
        assert http.session.headers["X-Auth-Token"] == "test-token"

    def test_sets_content_type(self, http):
        assert http.session.headers["Content-Type"] == "application/json"

    def test_custom_timeout(self):
        client = HttpClient("tok", timeout=60)
        assert client.timeout == 60


class TestRaiseForStatus:
    def _response(self, status_code, text="error detail"):
        """
        Create a MagicMock representing an HTTP response with the given status and text.
        
        Parameters:
            status_code (int): HTTP status code to set on the mock response.
            text (str): Response body text to set on the mock response.
        
        Returns:
            MagicMock: A mock response with `ok` set to True for status codes < 400, and `status_code` and `text` attributes set accordingly.
        """
        resp = MagicMock()
        resp.ok = status_code < 400
        resp.status_code = status_code
        resp.text = text
        return resp

    def test_ok_does_nothing(self):
        HttpClient._raise_for_status(self._response(200))

    def test_400_raises(self):
        with pytest.raises(UbidotsError400) as exc_info:
            HttpClient._raise_for_status(self._response(400))
        assert exc_info.value.status_code == 400

    def test_401_raises_forbidden(self):
        with pytest.raises(UbidotsForbiddenError):
            HttpClient._raise_for_status(self._response(401))

    def test_403_raises_forbidden(self):
        with pytest.raises(UbidotsForbiddenError):
            HttpClient._raise_for_status(self._response(403))

    def test_404_raises(self):
        with pytest.raises(UbidotsError404):
            HttpClient._raise_for_status(self._response(404))

    def test_500_raises(self):
        with pytest.raises(UbidotsError500):
            HttpClient._raise_for_status(self._response(500))

    def test_502_raises_500(self):
        with pytest.raises(UbidotsError500):
            HttpClient._raise_for_status(self._response(502))

    def test_unknown_4xx_raises_generic(self):
        with pytest.raises(UbidotsHTTPError) as exc_info:
            HttpClient._raise_for_status(self._response(429))
        assert exc_info.value.status_code == 429


class TestHttpMethods:
    @patch("ubidots._http.HttpClient._request")
    def test_get(self, mock_req, http):
        http.get("http://example.com", params={"a": 1})
        mock_req.assert_called_once_with("GET", "http://example.com", params={"a": 1})

    @patch("ubidots._http.HttpClient._request")
    def test_post(self, mock_req, http):
        http.post("http://example.com", json={"k": "v"})
        mock_req.assert_called_once_with("POST", "http://example.com", json={"k": "v"})

    @patch("ubidots._http.HttpClient._request")
    def test_patch(self, mock_req, http):
        http.patch("http://example.com", json={"k": "v"})
        mock_req.assert_called_once_with("PATCH", "http://example.com", json={"k": "v"})

    @patch("ubidots._http.HttpClient._request")
    def test_delete(self, mock_req, http):
        http.delete("http://example.com")
        mock_req.assert_called_once_with("DELETE", "http://example.com")


class TestRequest:
    def test_returns_json(self, http):
        resp = MagicMock()
        resp.ok = True
        resp.status_code = 200
        resp.content = b'{"key": "val"}'
        resp.json.return_value = {"key": "val"}
        http.session.request = MagicMock(return_value=resp)

        result = http.get("http://example.com")
        assert result == {"key": "val"}

    def test_204_returns_none(self, http):
        resp = MagicMock()
        resp.ok = True
        resp.status_code = 204
        resp.content = b""
        http.session.request = MagicMock(return_value=resp)

        assert http.delete("http://example.com") is None
