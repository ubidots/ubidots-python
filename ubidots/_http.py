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
        """
        Initialize the HttpClient instance and configure its requests session.
        
        Parameters:
            token (str): Ubidots API token sent as the `X-Auth-Token` header for all requests.
            timeout (int): Default request timeout in seconds used when no timeout is provided to calls.
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        })

    def get(self, url, **kwargs):
        """
        Send a GET request to the specified URL.
        
        Additional keyword arguments are forwarded to the underlying requests call (for example, params, headers, or timeout).
        
        Parameters:
            url (str): The request URL.
        
        Returns:
            The parsed JSON response, or `None` if the response has no content or the status is 204.
        """
        return self._request("GET", url, **kwargs)

    def post(self, url, json=None, **kwargs):
        """
        Send a POST request to the specified URL using the client's session.
        
        Parameters:
            url (str): The request URL.
            json (optional): JSON-serializable body to include in the request.
            **kwargs: Additional options forwarded to the underlying request (e.g., headers, params, timeout).
        
        Returns:
            The parsed JSON response, or `None` for HTTP 204 responses or when the response has no content.
        """
        return self._request("POST", url, json=json, **kwargs)

    def put(self, url, json=None, **kwargs):
        """
        Send a PUT request to the specified URL with an optional JSON payload.
        
        Parameters:
            url (str): The target request URL.
            json (Any, optional): JSON-serializable body to include in the request.
        
        Returns:
            result (Any or None): `None` if the response has no content or the status is 204, otherwise the parsed JSON response.
        """
        return self._request("PUT", url, json=json, **kwargs)

    def patch(self, url, json=None, **kwargs):
        """
        Send a PATCH request to the specified URL with an optional JSON payload.
        
        Parameters:
            url (str): The target request URL.
            json (Any, optional): JSON-serializable payload to include in the request body.
            **kwargs: Additional keyword arguments forwarded to the underlying request (e.g., params, headers).
        
        Returns:
            The parsed JSON response, or None for HTTP 204 responses or when the response has no content.
        """
        return self._request("PATCH", url, json=json, **kwargs)

    def delete(self, url, **kwargs):
        """
        Send an HTTP DELETE request to the given URL.
        
        Parameters:
            url (str): Request URL.
        
        Returns:
            The parsed JSON response, or `None` if the response has no content (e.g., 204 No Content).
        """
        return self._request("DELETE", url, **kwargs)

    def _request(self, method, url, **kwargs):
        """
        Perform an HTTP request using the client's session and return the parsed JSON body or None for empty responses.
        
        Parameters:
            method (str): HTTP method to use (e.g., "GET", "POST").
            url (str): Request URL.
            **kwargs: Additional arguments passed to requests.Session.request. If `timeout` is not provided, the client's default timeout is applied.
        
        Returns:
            dict | list | None: The parsed JSON response body, or `None` when the response has no content (e.g., status 204).
        """
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method, url, **kwargs)
        self._raise_for_status(response)
        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    @staticmethod
    def _raise_for_status(response):
        """
        Raise a Ubidots-specific exception for non-success HTTP responses.
        
        Parameters:
            response (requests.Response): HTTP response whose status code and body determine the raised exception.
        
        Raises:
            UbidotsError400: If the response status code is 400; message uses the response body.
            UbidotsForbiddenError: If the response status code is 401 or 403; message uses the response body.
            UbidotsError404: If the response status code is 404; message uses the response body.
            UbidotsError500: If the response status code is 500 or greater; message uses the response body.
            UbidotsHTTPError: For any other non-success status codes; includes the status code and response body.
        """
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
