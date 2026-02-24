class UbidotsError(Exception):
    """Base exception for all Ubidots errors."""


class UbidotsHTTPError(UbidotsError):
    """Raised when the Ubidots API returns an error HTTP status."""

    def __init__(self, status_code, detail=""):
        """
        Initialize an HTTP-related Ubidots error with a status code and optional detail message.
        
        Parameters:
            status_code (int): HTTP status code associated with the error.
            detail (str): Optional human-readable detail about the error (default is empty string).
        
        Notes:
            Sets `.status_code` and `.detail` attributes and constructs the exception message as "HTTP {status_code}: {detail}".
        """
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class UbidotsError400(UbidotsHTTPError):
    """Bad request."""

    def __init__(self, detail=""):
        """
        Initialize a 400 Bad Request UbidotsHTTPError with an optional detail message.
        
        Parameters:
            detail (str): Additional human-readable information about the error. Defaults to an empty string.
        """
        super().__init__(400, detail)


class UbidotsError404(UbidotsHTTPError):
    """Resource not found."""

    def __init__(self, detail=""):
        """
        Create an UbidotsError404 indicating an HTTP 404 Not Found error.
        
        Parameters:
            detail (str): Optional additional detail to include in the error message.
        """
        super().__init__(404, detail)


class UbidotsError500(UbidotsHTTPError):
    """Internal server error."""

    def __init__(self, detail=""):
        """
        Create an UbidotsHTTPError representing an HTTP 500 Internal Server Error.
        
        Parameters:
            detail (str): Optional human-readable detail appended to the error message.
        """
        super().__init__(500, detail)


class UbidotsForbiddenError(UbidotsHTTPError):
    """Authentication or authorization failure (401/403)."""

    def __init__(self, detail=""):
        """
        Initialize a UbidotsForbiddenError representing an HTTP 403 Forbidden response.
        
        Parameters:
            detail (str): Optional detail message to include in the error (defaults to "").
        """
        super().__init__(403, detail)


class UbidotsInvalidInputError(UbidotsError):
    """Raised for client-side input validation failures."""
