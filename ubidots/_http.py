import requests

from .exceptions import (
    UbidotsError400,
    UbidotsError404,
    UbidotsError500,
    UbidotsForbiddenError,
    UbidotsHTTPError,
)

DEFAULT_TIMEOUT = 30


class HttpClient:
    """Thin wrapper around requests.Session with Ubidots auth and error handling."""

    def __init__(self, token, timeout=DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        })

    def get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def post(self, url, json=None, **kwargs):
        return self._request("POST", url, json=json, **kwargs)

    def put(self, url, json=None, **kwargs):
        return self._request("PUT", url, json=json, **kwargs)

    def patch(self, url, json=None, **kwargs):
        return self._request("PATCH", url, json=json, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        self._raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    @staticmethod
    def _raise_for_status(response):
        if response.ok:
            return

        try:
            detail = response.text
        except Exception:
            detail = ""

        status = response.status_code
        if status == 400:
            raise UbidotsError400(detail)
        if status in (401, 403):
            raise UbidotsForbiddenError(detail)
        if status == 404:
            raise UbidotsError404(detail)
        if status >= 500:
            raise UbidotsError500(detail)
        raise UbidotsHTTPError(status, detail)
