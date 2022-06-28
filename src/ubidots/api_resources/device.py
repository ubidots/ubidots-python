from ubidots.mixins import ApiResourceMixin, RequestsMixin


class Devices(RequestsMixin):
    _plural = "devices"

    @classmethod
    def list(cls, **filters):
        devices = cls.get(cls._plural, filters).get("results", [])
        return [ApiResourceMixin(device) for device in devices]

    @classmethod
    def new(cls, **props):
        device = ApiResourceMixin(props)
        return device

    @classmethod
    def create(cls, **props):
        device = cls.post(f"{cls._plural}", props)
        return ApiResourceMixin(device)

    @classmethod
    def modify(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        device = cls.patch(f"{cls._plural}/{key}", props)
        return ApiResourceMixin(device)

    @classmethod
    def update(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        device = cls.put(f"{cls._plural}/{key}", props)
        return ApiResourceMixin(device)

    @classmethod
    def retrieve(cls, id: str = "", label: str = "", fields: list = []):
        key = cls._entity_key(id, label)
        device = cls.get(f"{cls._plural}/{key}", fields)
        return ApiResourceMixin(device)

    @classmethod
    def delete(cls, id: str = "", label: str = ""):
        key = cls._entity_key(id, label)
        cls.delete(f"{cls._plural}/{key}")

    @staticmethod
    def _entity_key(id: str = "", label: str = ""):
        return id if id else "~" + label
