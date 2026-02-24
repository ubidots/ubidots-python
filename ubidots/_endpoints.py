DEFAULT_BASE_URL = "https://industrial.api.ubidots.com"

V2_PREFIX = "/api/v2.0"
V1_PREFIX = "/api/v1.6"


class Endpoints:
    """URL builders for Ubidots v1.6 and v2.0 APIs."""

    def __init__(self, base_url=DEFAULT_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def _v2(self, path):
        return f"{self.base_url}{V2_PREFIX}{path}"

    def _v1(self, path):
        return f"{self.base_url}{V1_PREFIX}{path}"

    # ── Device CRUD (v2.0) ──

    def devices_url(self, label=None):
        if label:
            return self._v2(f"/devices/~{label}/")
        return self._v2("/devices/")

    def device_by_id_url(self, device_id):
        return self._v2(f"/devices/{device_id}/")

    # ── Variable CRUD (v2.0) ──

    def variables_url(self, label=None, device_label=None):
        if device_label and label:
            return self._v2(f"/devices/~{device_label}/variables/~{label}/")
        if device_label:
            return self._v2(f"/devices/~{device_label}/variables/")
        if label:
            return self._v2(f"/variables/~{label}/")
        return self._v2("/variables/")

    # ── Data ingestion/extraction (v1.6) ──

    def device_data_url(self, device_label):
        return self._v1(f"/devices/{device_label}")

    def variable_data_url(self, device_label, variable_label):
        return self._v1(f"/devices/{device_label}/{variable_label}/values")

    def variable_lv_url(self, device_label, variable_label):
        return self._v1(f"/devices/{device_label}/{variable_label}/lv")
