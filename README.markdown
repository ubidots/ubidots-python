#Ubidots Api Client

The Ubidots Python API Client makes calls to the [Ubidots Api](http://app.ubidots.com/api/).  The module is available on PyPi as [ubidots](http://pypi.python.org/pypi/ubidots/).


##Quick Start

1. Create an account in [Ubidots](http://ubidots.com) if you don't have one.

1. Create de directory myfirstdirective.

1. Install ubidots.

``
pip install ubidots
``


1. go to [ubidots](http://app.ubidots.com/userdata/api/) and copy your apikey into a file called apikey.txt inside myfirsdirective directory.

1. inside myfirstdatasource create the file myfirstdirective.py and copy the next code:

```python
from ubidots import ApiClient
import random


apikey = None
with open('apikey.txt') as f:
	apikey =  f.readline()

#Create an instance of the client with your apikey
api = ApiClient(apikey)

#Create your fist datasource
ds = api.create_datasource({'name':'firstds'})

#Create your first variable
var =  ds.create_variable({'name':'firstvar', 'unit':'rand'})

#Create 10 new values in your new variable
for i in range(10):
	var.save_value({'value':random.randint(1,10)})
```
1. runit:
```shell
$ python myfirstdirective.py
```

1. Thats all!!!

No you can go to [ubidots](http://app.ubidots.com) and under the data tab you can see your datasource, your variable and your posted values!
