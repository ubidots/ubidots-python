class ApiError(Exception):
    def __repr__(self):
        return f"{self.status_code} {self.status_message}"

    def __str__(self):
        return repr(self)


class ApiErrorBadRequest(ApiError):
    status_code = 400
    status_message = "Bad Request"


class ApiErrorUnauthorized(ApiError):
    status_code = 401
    status_message = "Unauthorized"


class ApiErrorPaymentRequired(ApiError):
    status_code = 402
    status_message = "Payment Required"


class ApiErrorForbidden(ApiError):
    status_code = 403
    status_message = "Forbidden"


class ApiErrorPageNotFound(ApiError):
    status_code = 404
    status_message = "Page Not Found"


class ApiErrorMethodNotAllowed(ApiError):
    status_code = 405
    status_message = "Method Not Allowed"


class ApiErrorConflict(ApiError):
    status_code = 409
    status_message = "Conflict"


class ApiErrorUnsupportedMediaType(ApiError):
    status_code = 415
    status_message = "Unsupported Media Type"


class ApiErrorServer(ApiError):
    status_code = 500
    status_message = "Server Error"
