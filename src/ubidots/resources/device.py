from src.ubidots.mixins import RequestsMixin
from src.ubidots.resource import Resource


class Device(RequestsMixin):
    _plural = "devices"

    @classmethod
    def create(cls, label: str = "", **kwargs):
        key = "~" + label
        if label:
            kwargs["label"] = label
        device = cls.post(f"{cls._plural}", **kwargs)
        return Resource(device)

    @classmethod
    def modify(cls, id: str = "", label: str = "", **kwargs):
        key = id if id else "~" + label
        if id:
            kwargs["id"] = id
        if label:
            kwargs["label"] = label
        device = cls.patch(f"{cls._plural}", **kwargs)
        return Resource(device)

    @classmethod
    def update(cls, id: str = "", label: str = "", **kwargs):
        key = id if id else "~" + label
        if id:
            kwargs["id"] = id
        if label:
            kwargs["label"] = label
        device = cls.put(f"{cls._plural}", **kwargs)
        return Resource(device)

    @classmethod
    def retrieve(cls, id: str = "", label: str = "", **kwargs):
        key = id if id else "~" + label
        device = cls.get(f"{cls._plural}/{key}", **kwargs)
        return Resource(device)

    @classmethod
    def delete(cls, id: str = "", label: str = ""):
        key = id if id else "~" + label
        cls.delete(f"{cls._plural}/{key}")
