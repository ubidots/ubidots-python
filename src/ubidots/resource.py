from src.ubidots.mixins import RequestsMixin


class Resource(RequestsMixin):
    _lazy = True

    def __init__(self, obj: dict):
        for key, val in obj.items():
            setattr(self, key, val)
