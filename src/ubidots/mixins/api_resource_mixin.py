from ubidots import api_client, data_api_ver


class ApiResourceMixin:
    def __init__(self, **props):
        for key, val in props.items():
            setattr(self, key, val)

    def send_data(self, *dot, **dots):
        path = "devices/"
        if hasattr(self, "device"):
            path += f"{self.device.label}/{self.label}/values"
        else:
            path += f"{self.label}"
        res = api_client.request(
            "POST", path, api_ver=data_api_ver, json=dot if dot else dots
        )
        return res.json()
