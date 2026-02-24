from ._endpoints import DEFAULT_BASE_URL, Endpoints
from ._http import HttpClient


class Ubidots:
    """Flat, label-based client for the Ubidots API.

    Uses v2.0 for device/variable CRUD and v1.6 for data ingestion/extraction.
    """

    def __init__(self, token, base_url=DEFAULT_BASE_URL, timeout=30):
        """
        Initialize the Ubidots client and configure internal HTTP and endpoint helpers.
        
        Parameters:
            token (str): API token used for authenticating requests.
            base_url (str): Base URL for the Ubidots API (defaults to DEFAULT_BASE_URL).
            timeout (int|float): Request timeout in seconds for the internal HTTP client.
        """
        self._http = HttpClient(token, timeout=timeout)
        self._endpoints = Endpoints(base_url)

    # ── Device management (v2.0) ──

    def get_devices(self, **params):
        """
        Retrieve devices from the API, applying optional query parameters.
        
        Parameters:
            params (dict): Optional query parameters forwarded to the devices endpoint (for example filters, page size, or pagination keys).
        
        Returns:
            list: A list of device objects (dict) aggregated across all paginated responses.
        """
        url = self._endpoints.devices_url()
        return self._paginate(url, params)

    def get_device(self, label):
        """
        Retrieve a device by its label.
        
        Parameters:
            label (str): The device's label.
        
        Returns:
            dict: The device representation returned by the API.
        """
        url = self._endpoints.devices_url(label)
        return self._http.get(url)

    def get_device_by_id(self, device_id):
        """
        Retrieve a device using its unique ID.
        
        Parameters:
            device_id: The device's unique identifier (string or int).
        
        Returns:
            dict: The device representation returned by the Ubidots API.
        """
        url = self._endpoints.device_by_id_url(device_id)
        return self._http.get(url)

    def create_device(self, *, label, name=None, **fields):
        """
        Create a device with the given label and optional name and additional fields.
        
        Parameters:
            label (str): Unique label for the device.
            name (str, optional): Human-readable name for the device.
            **fields: Additional device attributes to include in the request body.
        
        Returns:
            The API response for the created device.
        """
        url = self._endpoints.devices_url()
        body = {"label": label, **fields}
        if name is not None:
            body["name"] = name
        return self._http.post(url, json=body)

    def update_device(self, label, **fields):
        """
        Update fields of a device identified by its label.
        
        Parameters:
            label (str): Device label identifying the device to update.
            **fields: Device attributes to update; keys must match the API's device fields.
        
        Returns:
            The HTTP client's response for the PATCH request (API response).
        """
        url = self._endpoints.devices_url(label)
        return self._http.patch(url, json=fields)

    def delete_device(self, label):
        """
        Delete the device with the given label from the account.
        
        Parameters:
            label (str): The device's label.
        """
        url = self._endpoints.devices_url(label)
        self._http.delete(url)

    # ── Variable management (v2.0) ──

    def get_variables(self, device_label=None, **params):
        """
        Retrieve variables, optionally scoped to a specific device.
        
        Parameters:
        	device_label (str | None): If provided, return variables belonging to the device with this label; otherwise return variables across all devices.
        	**params: Additional query parameters forwarded to the variables endpoint (e.g., filters, page size).
        
        Returns:
        	variables (list[dict]): Aggregated list of variable resources returned by the API across all paginated pages.
        """
        url = self._endpoints.variables_url(device_label=device_label)
        return self._paginate(url, params)

    def get_variable(self, device_label, variable_label):
        """
        Retrieve a variable by label within a specific device.
        
        Parameters:
            device_label (str): Label of the device that contains the variable.
            variable_label (str): Label of the variable to retrieve.
        
        Returns:
            dict: The API response representing the variable resource.
        """
        url = self._endpoints.variables_url(variable_label, device_label=device_label)
        return self._http.get(url)

    def create_variable(self, device_label, *, label, name=None, **fields):
        """
        Create a new variable under the specified device.
        
        Parameters:
            device_label (str): Label of the device to create the variable for.
            label (str): Unique label for the new variable.
            name (str, optional): Human-readable name for the variable.
            **fields: Additional variable attributes to include in the request body (for example unit, tags, metadata).
        
        Returns:
            dict: The created variable resource as returned by the API.
        """
        url = self._endpoints.variables_url(device_label=device_label)
        body = {"label": label, **fields}
        if name is not None:
            body["name"] = name
        return self._http.post(url, json=body)

    def update_variable(self, device_label, variable_label, **fields):
        """
        Update fields of a variable belonging to a device.
        
        Parameters:
            device_label (str): Label of the device that contains the variable.
            variable_label (str): Label of the variable to update.
            **fields: Attributes to update on the variable (sent as JSON in the PATCH body).
        
        Returns:
            The HTTP client's response object from the PATCH request.
        """
        url = self._endpoints.variables_url(variable_label, device_label=device_label)
        return self._http.patch(url, json=fields)

    def delete_variable(self, device_label, variable_label):
        """
        Delete a variable from a device by label.
        
        Parameters:
            device_label (str): Label of the device containing the variable.
            variable_label (str): Label of the variable to delete.
        """
        url = self._endpoints.variables_url(variable_label, device_label=device_label)
        self._http.delete(url)

    # ── Data ingestion/extraction (v1.6) ──

    def send_values(self, device_label, data):
        """
        Send multiple variable readings to a device's data endpoint.
        
        Parameters:
            device_label (str): Label of the target device.
            data (dict | list): Payload to send as the JSON body; must be formatted according to Ubidots v1.6 device data ingestion.
        
        Returns:
            The HTTP response returned by the internal HTTP client.
        """
        url = self._endpoints.device_data_url(device_label)
        return self._http.post(url, json=data)

    def send_value(self, device_label, variable_label, value):
        """
        Send a single value for a device variable to the Ubidots ingestion endpoint.
        
        Parameters:
            device_label (str): Label of the target device.
            variable_label (str): Label of the target variable on the device.
            value (any | dict): If a dict is provided it is used as the JSON body; otherwise the value is wrapped as {"value": value}.
        
        Returns:
            The HTTP response returned by the API.
        """
        url = self._endpoints.variable_data_url(device_label, variable_label)
        body = value if isinstance(value, dict) else {"value": value}
        return self._http.post(url, json=body)

    def get_values(self, device_label, variable_label, **params):
        """
        Retrieve data points for a variable belonging to a device.
        
        Parameters:
            device_label (str): Label of the device that owns the variable.
            variable_label (str): Label of the variable to fetch data for.
            **params: Additional query parameters forwarded to the API (for example `start`, `end`, `limit`, or aggregation options).
        
        Returns:
            dict: The API response parsed as a Python object (typically a dict) containing the variable's data points.
        """
        url = self._endpoints.variable_data_url(device_label, variable_label)
        return self._http.get(url, params=params)

    def get_last_value(self, device_label, variable_label):
        """
        Fetches the most recent value for a variable on a device.
        
        @returns dict: The API response containing the latest value record for the specified variable.
        """
        url = self._endpoints.variable_lv_url(device_label, variable_label)
        return self._http.get(url)

    # ── Internal ──

    def _paginate(self, url, params):
        """
        Aggregate paginated GET responses from an API endpoint into a single list.
        
        Parameters:
            url (str): Initial endpoint URL to request.
            params (Mapping): Query parameters applied to the first request; subsequent pages follow `next` URLs and ignore these params.
        
        Returns:
            list: Concatenated list of items from each page's `"results"` field (empty list if none).
        """
        results = []
        params = dict(params)
        while url:
            data = self._http.get(url, params=params)
            results.extend(data.get("results", []))
            url = data.get("next")
            params = {}  # next URL already contains query params
        return results
