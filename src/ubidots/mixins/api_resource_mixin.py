from ubidots import api_client, data_api_ver


class ApiResourceMixin:
    def __init__(self, props: dict):
        for key, val in props.items():
            setattr(self, key, val)

    def send_data(self, **dots):
        path = f"devices/{self.label}/"
        res = api_client.request("POST", path, api_ver=data_api_ver, json=dots)
        return res.json()
