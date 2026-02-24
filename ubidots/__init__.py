__version__ = "2.0.0"

from .client import Ubidots
from .exceptions import (
    UbidotsError,
    UbidotsError400,
    UbidotsError404,
    UbidotsError500,
    UbidotsForbiddenError,
    UbidotsHTTPError,
    UbidotsInvalidInputError,
)
