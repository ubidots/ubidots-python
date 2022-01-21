from src.ubidots.client import api_client


class RequestsMixin:
    @staticmethod
    def get(path, **kwargs):
        response = api_client.get(path, params=kwargs)
        return response.json()

    @staticmethod
    def post(path, **kwargs):
        response = api_client.post(path, json=kwargs)
        return response.json()

    @staticmethod
    def put(path, **kwargs):
        response = api_client.put(path, json=kwargs)
        return response.json()

    @staticmethod
    def patch(path, **kwargs):
        response = api_client.patch(path, json=kwargs)
        return response.json()

    @staticmethod
    def delete(path):
        response = api_client.delete(path)
