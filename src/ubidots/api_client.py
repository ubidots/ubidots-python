from urllib.parse import urljoin

import requests

from . import config
from .error import *


def __getattr__(name: str):
    return getattr(_session, name)


def _handle_response_code(code):
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
    url = urljoin(_api_url, path)
    headers = {"X-Auth-Token": config.token}
    rsp = _request(method, url, headers=headers, **kwargs)
    try:
        rsp.raise_for_status()
    except requests.HTTPError:
        _handle_response_code(rsp.status_code)
    return rsp


_api_url = urljoin(config.base_url, f"api/{config.api_ver}/")
_session = requests.Session()
_request, _session.request = _session.request, request
