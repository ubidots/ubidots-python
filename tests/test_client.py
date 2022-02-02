import pytest
import responses

import ubidots
from ubidots import api_client


REQUEST_VERBS = ["GET", "POST", "PATCH", "PUT", "DELETE"]


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__auth_header(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(mocked_verb, f"{API_URL}/{ENDPOINT}", status=200)

    response = request_func(ENDPOINT)

    assert 200 == response.status_code
    assert "X-Auth-Token" in response.request.headers
    assert TOKEN == response.request.headers["X-Auth-Token"]

    ubidots.config.token = "other-token"

    response = request_func(ENDPOINT)

    assert 200 == response.status_code
    assert "X-Auth-Token" in response.request.headers
    assert "other-token" == response.request.headers["X-Auth-Token"]


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_400_bad_request(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=400,
        headers={"Content-Type": "application/json"},
        json={"code": 400001, "message": "400 Bad Request", "detail": ""},
    )

    with pytest.raises(ubidots.ApiErrorBadRequest, match=r"^400 Bad Request"):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_401_unauthorized(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=401,
        headers={"Content-Type": "application/json"},
        json={"code": 401001, "message": "401 Unauthorized", "detail": ""},
    )

    with pytest.raises(
        ubidots.ApiErrorUnauthorized, match=r"^401 Unauthorized"
    ):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_402_payment_required(
    mocked_responses, request_verb
):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=402,
        headers={"Content-Type": "application/json"},
        json={"code": 402001, "message": "402 Payment Required", "detail": ""},
    )

    with pytest.raises(
        ubidots.ApiErrorPaymentRequired, match=r"^402 Payment Required"
    ):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_403_forbidden(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=403,
        headers={"Content-Type": "application/json"},
        json={"code": 403001, "message": "403 Forbidden", "detail": ""},
    )

    with pytest.raises(ubidots.ApiErrorForbidden, match=r"^403 Forbidden"):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_404_page_not_found(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=404,
        headers={"Content-Type": "application/json"},
        json={"code": 404001, "message": "404 Page Not Found", "detail": ""},
    )

    with pytest.raises(
        ubidots.ApiErrorPageNotFound, match=r"^404 Page Not Found"
    ):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_405_method_not_allowed(
    mocked_responses, request_verb
):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=405,
        headers={"Content-Type": "application/json"},
        json={
            "code": 405001,
            "message": "405 Method Not Allowed",
            "detail": "",
        },
    )

    with pytest.raises(
        ubidots.ApiErrorMethodNotAllowed, match=r"^405 Method Not Allowed"
    ):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_409_conflict(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=409,
        headers={"Content-Type": "application/json"},
        json={"code": 409001, "message": "409 Conflict", "detail": ""},
    )

    with pytest.raises(ubidots.ApiErrorConflict, match=r"^409 Conflict"):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_415_unsupported_media_type(
    mocked_responses, request_verb
):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=415,
        headers={"Content-Type": "application/json"},
        json={
            "code": 415001,
            "message": "415 Unsupported Media Type",
            "detail": "",
        },
    )

    with pytest.raises(
        ubidots.ApiErrorUnsupportedMediaType,
        match=r"^415 Unsupported Media Type",
    ):
        response = request_func(ENDPOINT)


@pytest.mark.parametrize("request_verb", REQUEST_VERBS)
def test__raise_exception_on_5xx_server_error(mocked_responses, request_verb):
    TOKEN = "my-token"
    API_URL = f"{ubidots.config.base_url}/api/{ubidots.config.api_ver}"
    ENDPOINT = "endpoint"

    ubidots.config.token = TOKEN

    request_func = getattr(api_client, request_verb.lower())
    mocked_verb = getattr(responses, request_verb.upper())
    mocked_responses.add(
        mocked_verb,
        f"{API_URL}/{ENDPOINT}",
        status=500,
        headers={"Content-Type": "application/json"},
        json={
            "code": 500001,
            "message": "500 Server Error",
            "detail": "",
        },
    )

    with pytest.raises(ubidots.ApiErrorServer, match=r"^500 Server Error"):
        response = request_func(ENDPOINT)
