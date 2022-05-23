from ubidots import api_client


class RequestsMixin:
    @staticmethod
    def get(path, query_params):
        response = api_client.get(path, params=query_params)
        return response.json()

    @staticmethod
    def post(path, body_params):
        response = api_client.post(path, json=body_params)
        return response.json()

    @staticmethod
    def put(path, body_params):
        response = api_client.put(path, json=body_params)
        return response.json()

    @staticmethod
    def patch(path, body_params):
        response = api_client.patch(path, json=body_params)
        return response.json()

    @staticmethod
    def delete(path):
        response = api_client.delete(path)
