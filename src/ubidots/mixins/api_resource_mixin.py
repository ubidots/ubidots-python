from .mixins import RequestsMixin


class Resource(RequestsMixin):
    def __init__(self, obj: dict):
        for key, val in obj.items():
            setattr(self, key, val)
