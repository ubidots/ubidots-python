# ubidots-python

Python client for the [Ubidots](https://ubidots.com) API.

## Installation

```bash
pip install ubidots
```

Requires Python 3.8+.

## Quick Start

```python
from ubidots import Ubidots

api = Ubidots(token="BBFF-xxxxx")

# Send multiple variables to a device in one call
api.send_values("weather-station", {
    "temperature": 22.5,
    "humidity": 60,
    "pressure": 1013.25,
})

# Get the last value of a variable
temp = api.get_last_value("weather-station", "temperature")
print(temp)
```

## Usage

### Connecting

```python
from ubidots import Ubidots

api = Ubidots(token="BBFF-xxxxx")

# For on-premise / custom deployments:
api = Ubidots(token="BBFF-xxxxx", base_url="https://my-ubidots.example.com")
```

### Sending Data

```python
# Send multiple variables at once (most common)
api.send_values("weather-station", {
    "temperature": 22.5,
    "humidity": 60,
})

# Send a single value
api.send_value("weather-station", "temperature", 22.5)

# Send a value with timestamp and context
api.send_value("weather-station", "temperature", {
    "value": 22.5,
    "timestamp": 1609459200000,
    "context": {"lat": 6.25, "lng": -75.56},
})
```

### Reading Data

```python
# Get the last value of a variable
temp = api.get_last_value("weather-station", "temperature")

# Get historical values
values = api.get_values("weather-station", "temperature")
```

### Device Management

```python
api.create_device(label="weather-station", name="Weather Station")
device = api.get_device("weather-station")
devices = api.get_devices()
api.update_device("weather-station", name="New Name")
api.delete_device("weather-station")
```

### Variable Management

```python
api.create_variable("weather-station", label="temperature", name="Temperature")
variable = api.get_variable("weather-station", "temperature")
variables = api.get_variables("weather-station")
api.delete_variable("weather-station", "temperature")
```

### Error Handling

```python
from ubidots import Ubidots, UbidotsError404, UbidotsForbiddenError

api = Ubidots(token="BBFF-xxxxx")

try:
    device = api.get_device("nonexistent")
except UbidotsError404:
    print("Device not found")
except UbidotsForbiddenError:
    print("Invalid token or insufficient permissions")
```

## API Reference

All methods use **labels** to identify devices and variables. The library handles the `~` prefix for label-based lookups in v2.0 endpoints automatically.

| Method | Description |
|--------|-------------|
| `send_values(device_label, data)` | Send multiple variable values to a device |
| `send_value(device_label, variable_label, value)` | Send a single value |
| `get_last_value(device_label, variable_label)` | Get the last value of a variable |
| `get_values(device_label, variable_label, **params)` | Get historical values |
| `get_devices(**params)` | List all devices |
| `get_device(label)` | Get a device by label |
| `create_device(*, label, name=None, **fields)` | Create a device |
| `update_device(label, **fields)` | Update a device |
| `delete_device(label)` | Delete a device |
| `get_variables(device_label=None, **params)` | List variables |
| `get_variable(device_label, variable_label)` | Get a variable by label |
| `create_variable(device_label, *, label, name=None, **fields)` | Create a variable |
| `update_variable(device_label, variable_label, **fields)` | Update a variable |
| `delete_variable(device_label, variable_label)` | Delete a variable |

## License

MIT - see [LICENSE](LICENSE) for details.
