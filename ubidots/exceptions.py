class UbidotsError(Exception):
    """Base exception for all Ubidots errors."""


class UbidotsHTTPError(UbidotsError):
    """Raised when the Ubidots API returns an error HTTP status."""

    def __init__(self, status_code, detail=""):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class UbidotsError400(UbidotsHTTPError):
    """Bad request."""

    def __init__(self, detail=""):
        super().__init__(400, detail)


class UbidotsError404(UbidotsHTTPError):
    """Resource not found."""

    def __init__(self, detail=""):
        super().__init__(404, detail)


class UbidotsError500(UbidotsHTTPError):
    """Internal server error."""

    def __init__(self, detail=""):
        super().__init__(500, detail)


class UbidotsForbiddenError(UbidotsHTTPError):
    """Authentication or authorization failure (401/403)."""

    def __init__(self, detail=""):
        super().__init__(403, detail)


class UbidotsInvalidInputError(UbidotsError):
    """Raised for client-side input validation failures."""
