# Ubidots Python SDK


## Usage

### Send data to device

```python
import ubidots

ubidots.token = "<token>"

# Create device instance locally but not on Ubidots
device = ubidots.Devices.new(label="my-device")

# Send single variable value
device.send_data(temperature=10)

# Send multiple variables values
device.send_data(temperature=10, humidity=90, pressure=78)

# Send single variable dot
temperature = {
	"value": 10,
	"timestamp": 1634311791000,
	"context": {"status": "cold"},
}
device.send_data(temperature=temperature)

# Send multiple variables dots
temperature = {
	"value": 10,
	"timestamp": 1634311791000,
	"context": {"status": "cold"},
}
humidity = {
	"value": 90,
	"timestamp": 1634311791000,
	"context": {"status": "High humidity"},
}
pressure = {
	"value": 78,
	"timestamp": 1634311791000,
	"context": {"status": "Normal"},
}
device.send_data(temperature=temperature, humidity=humidity, pressure=pressure)

# Send position
position = {"value": 1, "context": {"lat": 6.5423, "lng": -70.5783}}
device.send_data(position=position)
```

### Send data to device variable

```python
import ubidots

ubidots.token = "<token>"

# Create device instance locally but not on Ubidots
device = ubidots.Devices.new(label="my-device")
# Create variable instance locally but not on Ubidots
variable = device.Variables.new(label="my-variable")

# Send single variable value
variable.send_data(value=10)

# Send single variable dot
variable.send_data(value=10, timestamp=1634311791000, context={"status": "cold"})

# Send multiple variable dots
dots = [
	{
		"value": 10,
		"timestamp": 1634311791000,
		"context": {"status": "cold"},
	},
	{
		"value": 12,
		"timestamp": 1634311891000,
		"context": {"status": "cold"},
	},
	{
		"value": 14,
		"timestamp": 1634311991000,
		"context": {"status": "cold"},
	},
]
variable.send_data(*dots)

# Send position
position = {"value": 1, "context": {"lat": 6.5423, "lng": -70.5783}}
variable.send_data(**position)
```

## Development

### Run tests

```
tox
```
