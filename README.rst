===================================
Ubidots Python Api Client
===================================

The Ubidots Python API Client makes calls to the `Ubidots Api <http://things.ubidots.com/api>`_  The module is available on PyPi_ as  ubidots


Quick Start
===========

#. Create an account in `Ubidots <http://ubidots.com>`_ if you don't
   have one.

#. Create de directory myfirstdirective.

#. Install ubidots.

   .. code-block:: bash

      $ pip install ubidots


#. Go to your api_ spot and copy your apikey into a file called
   apikey.txt inside myfirsdirective directory.
#. Inside myfirstdatasource create the file myfirstdirective.py and
   copy the next code:

   .. code-block:: python

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


#. Run it:

   .. code-block:: bash

      $ python myfirstdirective.py

#. Thats all!!!

No you can go to `your account <http://app.ubidots.com>`_ in Ubitods
and under the data tab you can see your datasource, your variable and
your posted values!



.. _PyPi: http://pypi.python.org/pypi/ubidots/
.. _api: http://app.ubidots.com/userdata/api/
