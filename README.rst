===================================
Ubidots Python API Client
===================================

The Ubidots Python API Client makes calls to the `Ubidots Api <http://things.ubidots.com/api>`_.  The module is available on `PyPI <https://pypi.python.org/pypi/ubidots/>`_ as "ubidots".

To follow this quickstart you'll need to install python 2.7 in your machine (either be it a computer or an python-capable device), you can find more details in `<http://www.python.org/download/>`_.


Installing the Python library
-----------------------------

Ubidots for python is available in PyPI and you can install it from the command line:

.. code-block:: bash

    $ pip install ubidots==1.6.1

Don't forget to use sudo if necessary.

You can install pip in Linux and Mac using this command:

.. code-block:: bash

    $ sudo easy_install pip

If you don't have *easy_install*, you can get it through *apt-get* on Debian-based distributions:

.. code-block:: bash
    
    $ sudo apt-get install python-setuptools

If you are using Microsoft Windows you can install pip from `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip>`_.


Connecting to the API
----------------------

Before playing with the API you must be able to connect to it using your private API key, which can be found `in your profile <http://app.ubidots.com/userdata/api/>`_.

If you don't have an account yet, you can `create one here <http://app.ubidots.com/accounts/signup/>`_.

Once you have your API key, you can connect to the API by creating an ApiClient instance. Let's assume your API key is: "7fj39fk3044045k89fbh34rsd9823jkfs8323". Then your code would look like this:


.. code-block:: python

    from ubidots import ApiClient

    api = ApiClient('7fj39fk3044045k89fbh34rsd9823jkfs8323')


Now you have an instance of ApiClient ("api") which can be used to connect to the API service.

Saving a new Value to a Variable
--------------------------------

Retrieve the variable you'd like the value to be saved to:

.. code-block:: python

    my_variable = api.get_variable('56799cf1231b28459f976417')

Given the instantiated variable, you can save a new value with the following line:

.. code-block:: python

    new_value = my_variable.save_value({'value': 10})

You can also specify a timestamp (optional):

.. code-block:: python

    new_value = my_variable.save_value({'value': 10, 'timestamp': 1376061804407})

If no timestamp is specified, the API server will assign the current time to it. We think it's always better if you specify the timestamp so that the record reflects the exact time when the value was captured, and not the time it got to our servers.

Creating a DataSource
----------------------

As you might know by now, a data source represents a device or a virtual source.

This line creates a new data source:

.. code-block:: python

    new_datasource = api.create_datasource({"name": "myNewDs", "tags": ["firstDs", "new"], "description": "any des"})


The name key is required, but the tags and description keys are optional. This new data source can be used to track different variables, so let's create one.


Creating a Variable
--------------------

A variable is a time-series containing different values over time. Let's create one:


.. code-block:: python

    new_variable = new_datasource.create_variable({"name": "myNewVar", "unit": "Nw"})

The name and unit keys are required.

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

To get the values of a variable, use the method get_values in an instance of the class Variable. This will return a list like object with an aditional attribute items_in_server that tells you how many values this variable has stored on the server.

If you only want the last N values call the method with the number of elements you want.

.. code-block:: python

    # Getting all the values from the server. Note that this could result in a
    # lot of requests, and potentially violate your requests per second limit.
    all_values = new_variable.get_values()
    
    # If you want just the last 100 values you can use:
    some_values = new_variable.get_values(100)
    

Getting a group of Data sources
--------------------------------

If you want to get all your data sources you can use the instance of the api directly, remember, given that the
items are returned with pagination from the server, this method return a Paginator object that you can use
to iterate throught the items:

.. code-block:: python
    
    #get all datasources
    all_datasources = api.get_datasources()
    
    #get_the last 5 created datasources
    some_datasources = api.get_datasources(5)


Getting a specific Data source
-------------------------------

Each data source has a unique id that tells the server which one to retrieve.

For example, if a data source has the id 51c99cfdf91b28459f976414, it can be retrieved using the method get_datasource of the ApiClient instance:


.. code-block:: python

    my_specific_datasource = api.get_datasource('51c99cfdf91b28459f976414')


Getting a group of  Variables from a Data source
-------------------------------------------------

You can also retrieve all the variables of a data source:

.. code-block:: python

    #get all variables
    all_variables =  datasource.get_variables()
    
    #get last 10 variables
    some_variables =  datasource.get_variables(10)


Getting a specific Variable
------------------------------

As with data sources, use your variable's id to retrieve the details about a variable:

.. code-block:: python

    my_specific_variable = api.get_variable('56799cf1231b28459f976417')


Managing HTTP Exceptions
-------------------------

Given that some errors would happen when a request is made to Ubidots, the api client has some built in exceptions
to make easier to spot the problems, the exceptions are:

UbidotsError400, UbidotsError404, UbidotsError500, UbidotsForbiddenError,
UbidotsBulkOperationError

each error has the attributes:
message: for a general message of the error.
detail: generally a json from the server explaining in more detail the error.

you can use those exceptions in this way:

.. code-block:: python

    try:
        my_specific_variable = api.get_variable('56799cf1231b28459f976417')
    except UbidotsError400 as e:
        print "General Description: %s; and the detail: %s" % (e.message, e.detail)
    except UbidotsForbiddenError as e:
        print "For some reason my account does not have permission to read this variable"
        print "General Description: %s; and the detail: %s" % (e.message, e.detail)

Other Exceptions
----------------

There is anoter exception UbidotsInvalidInputError wich is raised when the fields to create a Datasource a Variable
or a Value are not complete.

For this version of the api the the fields for each resource are:

Datasource:
   Required:
       name: string.
   Optional:
       tags: list of strings.

       description: string.

Variables:
    Required:
        name: string.
        
        unit: string.

Values:
    Required:
        value: number (integer or float).
        
        variable: string with the variable of the id id.
    Optional:
        timestamp: unix timestamp.
