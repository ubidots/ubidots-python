from ubidots.mixins import ApiResourceMixin, RequestsMixin


class Variables(RequestsMixin):
    _plural = "variables"

    @classmethod
    def list(cls, **filters):
        variables = cls.get(cls._plural, filters).get("results", [])
        return [ApiResourceMixin(variable) for variable in variables]

    @classmethod
    def create(cls, **props):
        variable = cls.post(f"{cls._plural}", props)
        return ApiResourceMixin(variable)

    @classmethod
    def modify(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        variable = cls.patch(f"{cls._plural}/{key}", props)
        return ApiResourceMixin(variable)

    @classmethod
    def update(cls, **props):
        key = cls._entity_key(props.get("id"), props.get("label"))
        variable = cls.put(f"{cls._plural}/{key}", props)
        return ApiResourceMixin(variable)

    @classmethod
    def retrieve(cls, id: str = "", label: str = "", fields: list = []):
        key = cls._entity_key(id, label)
        variable = cls.get(f"{cls._plural}/{key}", fields)
        return ApiResourceMixin(variable)

    @classmethod
    def delete(cls, id: str = "", label: str = ""):
        key = cls._entity_key(id, label)
        cls.delete(f"{cls._plural}/{key}")

    @staticmethod
    def _entity_key(id: str = "", label: str = ""):
        return id if id else "~" + label
