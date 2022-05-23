import atexit
from urllib.parse import urljoin

import requests

import ubidots
from ubidots.error import *


def __getattr__(name: str):
    return getattr(_session, name)


def _handle_response_code(code: int):
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


def request(method: str, path: str, **kwargs):
    api_url = urljoin(ubidots.base_url, f"api/{ubidots.api_ver}/")
    url = urljoin(api_url, path)
    headers = {"X-Auth-Token": ubidots.token}
    rsp = _request(method, url, headers=headers, **kwargs)
    try:
        rsp.raise_for_status()
    except requests.HTTPError:
        _handle_response_code(rsp.status_code)
    return rsp


_session = requests.Session()
_session.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
_request, _session.request = _session.request, request

atexit.register(_session.close)
