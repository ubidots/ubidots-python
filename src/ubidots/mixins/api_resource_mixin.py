class ApiResourceMixin:
    def __init__(self, obj: dict):
        for key, val in obj.items():
            setattr(self, key, val)
