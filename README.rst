===================================
Ubidots Python API Client
===================================

The Ubidots Python API Client makes calls to the `Ubidots Api <http://things.ubidots.com/api>`_.  The module is available on `PyPi <https://pypi.python.org/pypi/ubidots/>`_ as "ubidots".

To follow this quickstart you'll need to install python 2.7 in your machine (either be it a computer or an python-capable device), you can find more details in `<http://www.python.org/download/>`_.


Installing the Python library
-----------------------------

Ubidots for python is available in Pypi and you can install it from the command line:

.. code-block:: bash

    $ pip install ubidots

Don't forget to use sudo if necessary.

You can install pip in Linux and Mac using this command:

.. code-block:: bash

    $ easy_install pip

If you are using Microsoft Windows you can install pip from `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip>`_.


Connecting to the API
----------------------

Before playing with the API you must be able to connect to it using your private API key, which can be found `in your profile <http://app.ubidots.com/userdata/api/>`_.

If you don't have an account yet, you can `create one here <http://app.ubidots.com/accounts/signup/>`_.

Once you have your API key, you can connect to the API by creating an ApiClient instance. Let's assume your API key is: "7fj39fk3044045k89fbh34rsd9823jkfs8323" then your code would look like this:


.. code-block:: python

    from ubidots import ApiClient

    api = ApiClient('7fj39fk3044045k89fbh34rsd9823jkfs8323')


Now you have an instance of the apiclient ("api") which can be used to connect to the API service.

Saving a new Value to a Variable
--------------------------------

Retrieve the variable you'd like the value to be saved to:

.. code-block:: python

    my_variable = api.get_variable(id = '56799cf1231b28459f976417')

Given the instantiated variable, you can save a new value with the following line:

.. code-block:: python

    new_value = my_variable.save_value({'value':10})

You can also specify a timestamp (optional)

.. code-block:: python

    new_value = my_variable.save_value({'value':10, 'timestamp':1376061804407})

If no timestamp is specified, the API server will assign the current time to it. We think it's always better that you specify the timestamp so that
it reflects the exact time when the value was captured, and not the time when it got to our servers.

Creating a DataSource
----------------------

As you might know by now, a data source represents a device or a virtual source.

This line creates a new data source:

.. code-block:: python

    new_datasource = api.create_datasource({"name":"myNewDs"})


This new data source can be used to track different variables, so let's create one.


Creating a Variable
--------------------

A variable is a time-series containing different values over time. Let's create one:


.. code-block:: python

    new_variable = new_datasource.create_variable({"name":"myNewVar"})



Saving Values in Bulk
---------------------

Values may also be added in bulk. This is especially useful when data is gathered offline and connection to the internet is limited.

.. code-block:: python

   new_variable.save_values([
       {'timestamp': 1380558972614, 'value': 20},
       {'timestamp': 1380558972915, 'value': 40},
       {'timestamp': 1380558973516, 'value': 50},
       {'timestamp': 1380558973617, 'value': 30}
   ])


Getting Values
--------------

To get the values for a variable, use the method get_values in an instance of the class Variable.

.. code-block:: python

    all_values = new_variable.get_values()


You may also want to get the last value of certain variable with this purpose, first you need to update the variable:

.. code-block:: python

    new_variable = api.get_variable(new_variable.id)
    last_value = new_variable.last_value

Getting all the Data sources
-----------------------------

If you want to get all your data sources you can use the instance of the api directly:

.. code-block:: python

    all_my_datasources = api.get_datasources()


Getting a specific Data source
------------------------------

Each data source has a unique id that tells the server which one to retrieve.

For example, if a data source has the id 51c99cfdf91b28459f976414, it can be retrieved using the method get_datasource of the ApiClient instance:


.. code-block:: python

    my_specific_datasource = api.get_datasource(id = '51c99cfdf91b28459f976414')


Getting All Variables from a Data source
-----------------------------------------

You can also retrieve all the variables of a data source:

.. code-block:: python

    all_datasource_variables = datasource.get_variables()


Getting a specific Variable
------------------------------

As with data sources, use your variable's id to retrieve the details about a variable:

.. code-block:: python

    my_specific_variable = api.get_variable(id = '56799cf1231b28459f976417')
