from ..mixins import RequestsMixin
from ..resource import Resource


class Device(RequestsMixin):
    _plural = "devices"

    @classmethod
    def create(cls, **props):
        device = cls.post(f"{cls._plural}", props)
        return Resource(device)

    @classmethod
    def modify(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        device = cls.patch(f"{cls._plural}/{key}", props)
        return Resource(device)

    @classmethod
    def update(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        device = cls.put(f"{cls._plural}/{key}", props)
        return Resource(device)

    @classmethod
    def retrieve(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        device = cls.get(f"{cls._plural}/{key}", props)
        return Resource(device)

    @classmethod
    def delete(cls, id: str = "", label: str = ""):
        key = cls._entity_key(props.get("id"), props.get("label"))
        cls.delete(f"{cls._plural}/{key}")

    @staticmethod
    def _entity_key(id: str = None, label: str = None):
        return id if id is not None else "~" + label
