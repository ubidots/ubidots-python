DEFAULT_BASE_URL = "https://industrial.api.ubidots.com"

V2_PREFIX = "/api/v2.0"
V1_PREFIX = "/api/v1.6"


class Endpoints:
    """URL builders for Ubidots v1.6 and v2.0 APIs."""

    def __init__(self, base_url=DEFAULT_BASE_URL):
        """
        Initialize the Endpoints instance with a sanitized base URL.
        
        Parameters:
            base_url (str): Base URL used for building API endpoints; any trailing '/' is removed before storage.
        """
        self.base_url = base_url.rstrip("/")

    def _v2(self, path):
        """
        Builds a full Ubidots v2.0 API URL for the given path.
        
        Parameters:
            path (str): Path relative to the v2 API prefix (e.g. '/devices' or '/devices/{id}'); may include a leading slash.
        
        Returns:
            url (str): Full URL for the v2.0 endpoint.
        """
        return f"{self.base_url}{V2_PREFIX}{path}"

    def _v1(self, path):
        """
        Build the full v1.6 API URL for the given path.
        
        Parameters:
            path (str): Path to append to the v1.6 API prefix (e.g., '/devices' or '/devices/<label>').
        
        Returns:
            str: Complete URL for the v1.6 endpoint.
        """
        return f"{self.base_url}{V1_PREFIX}{path}"

    # ── Device CRUD (v2.0) ──

    def devices_url(self, label=None):
        """
        Builds the v2.0 devices endpoint URL, optionally scoped to a specific device label.
        
        Parameters:
            label (str, optional): Device label to scope the endpoint to that device.
        
        Returns:
            str: Full URL for the devices endpoint; if `label` is provided, URL for the specified device.
        """
        if label:
            return self._v2(f"/devices/~{label}/")
        return self._v2("/devices/")

    def device_by_id_url(self, device_id):
        """
        Builds the v2.0 URL for a device identified by its ID.
        
        Parameters:
            device_id (str): Device identifier to include in the path.
        
        Returns:
            str: Full v2.0 endpoint URL for the specified device.
        """
        return self._v2(f"/devices/{device_id}/")

    # ── Variable CRUD (v2.0) ──

    def variables_url(self, label=None, device_label=None):
        """
        Builds a v2.0 API URL for variable resources, optionally scoped to a device or a specific variable label.
        
        Parameters:
            label (str | None): Variable label to target a specific variable; when provided with `device_label`, targets the variable within that device.
            device_label (str | None): Device label to scope the variables to a specific device.
        
        Returns:
            str: Full v2.0 endpoint URL:
                - If both `device_label` and `label` are provided: URL for a specific variable within the specified device.
                - If only `device_label` is provided: URL for all variables of the specified device.
                - If only `label` is provided: URL for the specific variable across devices.
                - If neither is provided: URL for the generic variables collection.
        """
        if device_label and label:
            return self._v2(f"/devices/~{device_label}/variables/~{label}/")
        if device_label:
            return self._v2(f"/devices/~{device_label}/variables/")
        if label:
            return self._v2(f"/variables/~{label}/")
        return self._v2("/variables/")

    # ── Data ingestion/extraction (v1.6) ──

    def device_data_url(self, device_label):
        """
        Build the v1.6 API URL for a device's data using its label.
        
        Parameters:
            device_label (str): The device's label used in the URL path.
        
        Returns:
            str: Full v1.6 endpoint URL for the device's data (e.g. ".../api/v1.6/devices/{device_label}").
        """
        return self._v1(f"/devices/{device_label}")

    def variable_data_url(self, device_label, variable_label):
        """
        Builds the v1.6 endpoint URL for the values of a specific variable on a specific device.
        
        Parameters:
            device_label (str): Label of the device containing the variable.
            variable_label (str): Label of the variable whose values are requested.
        
        Returns:
            str: Full v1.6 API URL for the variable's values (e.g. .../devices/{device_label}/{variable_label}/values).
        """
        return self._v1(f"/devices/{device_label}/{variable_label}/values")

    def variable_lv_url(self, device_label, variable_label):
        """
        Builds the v1.6 API URL for the latest value ("lv") of a specific variable on a device.
        
        Parameters:
            device_label (str): Label of the device containing the variable.
            variable_label (str): Label of the variable whose latest value is requested.
        
        Returns:
            str: Full v1.6 endpoint URL for the variable's latest value.
        """
        return self._v1(f"/devices/{device_label}/{variable_label}/lv")
