import requests
from urllib.parse import urljoin

from src import ubidots
from src.ubidots.error import *


class Client(requests.Session):
    def __init__(self, base_url, api_ver):
        super().__init__()
        self._base_url = base_url
        self._api_ver = api_ver
        self._api_url = urljoin(self._base_url, f"api/{self._api_ver}/")

    def __del__(self):
        self.close()

    def _handle_response_code(self, code):
        errors = {
            400: ApiErrorBadRequest,
            401: ApiErrorUnauthorized,
            402: ApiErrorPaymentRequired,
            403: ApiErrorForbidden,
            404: ApiErrorPageNotFound,
            405: ApiErrorMethodNotAllowed,
            409: ApiErrorConflict,
            415: ApiErrorUnsupportedMediaType,
            500: ApiErrorServer,
        }
        if code >= 200 and code < 300:
            return
        raise errors.get(code, ApiErrorBadRequest)

    def request(self, method: str, path: str, **kwargs):
        url = urljoin(self._api_url, path)
        headers = {"X-Auth-Token": ubidots.token}
        rsp = super().request(method, url, headers=headers, **kwargs)
        try:
            rsp.raise_for_status()
        except requests.HTTPError:
            self._handle_response_code(rsp.status_code)
        return rsp


api_client = Client(ubidots.base_url, ubidots.api_ver)
