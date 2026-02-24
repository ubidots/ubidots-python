from ._endpoints import DEFAULT_BASE_URL, Endpoints
from ._http import HttpClient


class Ubidots:
    """Flat, label-based client for the Ubidots API.

    Uses v2.0 for device/variable CRUD and v1.6 for data ingestion/extraction.
    """

    def __init__(self, token, base_url=DEFAULT_BASE_URL, timeout=30):
        self._http = HttpClient(token, timeout=timeout)
        self._endpoints = Endpoints(base_url)

    # ── Device management (v2.0) ──

    def get_devices(self, **params):
        url = self._endpoints.devices_url()
        return self._paginate(url, params)

    def get_device(self, label):
        url = self._endpoints.devices_url(label)
        return self._http.get(url)

    def get_device_by_id(self, device_id):
        url = self._endpoints.device_by_id_url(device_id)
        return self._http.get(url)

    def create_device(self, *, label, name=None, **fields):
        url = self._endpoints.devices_url()
        body = {"label": label, **fields}
        if name is not None:
            body["name"] = name
        return self._http.post(url, json=body)

    def update_device(self, label, **fields):
        url = self._endpoints.devices_url(label)
        return self._http.patch(url, json=fields)

    def delete_device(self, label):
        url = self._endpoints.devices_url(label)
        self._http.delete(url)

    # ── Variable management (v2.0) ──

    def get_variables(self, device_label=None, **params):
        url = self._endpoints.variables_url(device_label=device_label)
        return self._paginate(url, params)

    def get_variable(self, device_label, variable_label):
        url = self._endpoints.variables_url(variable_label, device_label=device_label)
        return self._http.get(url)

    def create_variable(self, device_label, *, label, name=None, **fields):
        url = self._endpoints.variables_url(device_label=device_label)
        body = {"label": label, **fields}
        if name is not None:
            body["name"] = name
        return self._http.post(url, json=body)

    def update_variable(self, device_label, variable_label, **fields):
        url = self._endpoints.variables_url(variable_label, device_label=device_label)
        return self._http.patch(url, json=fields)

    def delete_variable(self, device_label, variable_label):
        url = self._endpoints.variables_url(variable_label, device_label=device_label)
        self._http.delete(url)

    # ── Data ingestion/extraction (v1.6) ──

    def send_values(self, device_label, data):
        url = self._endpoints.device_data_url(device_label)
        return self._http.post(url, json=data)

    def send_value(self, device_label, variable_label, value):
        url = self._endpoints.variable_data_url(device_label, variable_label)
        body = value if isinstance(value, dict) else {"value": value}
        return self._http.post(url, json=body)

    def get_values(self, device_label, variable_label, **params):
        url = self._endpoints.variable_data_url(device_label, variable_label)
        return self._http.get(url, params=params)

    def get_last_value(self, device_label, variable_label):
        url = self._endpoints.variable_lv_url(device_label, variable_label)
        return self._http.get(url)

    # ── Internal ──

    def _paginate(self, url, params):
        results = []
        params = dict(params)
        while url:
            data = self._http.get(url, params=params)
            results.extend(data.get("results", []))
            url = data.get("next")
            params = {}  # next URL already contains query params
        return results
