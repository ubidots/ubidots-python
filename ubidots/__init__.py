
__version__ = '0.1.3-alpha'


class UbidotsLibraryError (Exception):
    pass

def check_requests_version():
	minimum_requests_version = '1.2.3'
	try:
		import requests
	except:
		raise UbidotsLibraryError("""requests Library is not installed, please install it
		with pip install requests or better yet install ubidots using pip install ubidots""")

	
	if requests.__version__ < '1.2.3':
		raise UbidotsLibraryError("""Your current version of the library requests is %s,
		    to work with Ubidots you need at least the version 1.2.3
		    you can install the latest version with 'pip install request' or better yet install
		    ubidots with 'pip install ubidots' """%requests.__version__ )


check_requests_version()

from apiclient import ApiClient, Datasource, Variable, ServerBridge, Paginator
from apiclient import UbidotsError400, UbidotsError404, UbidotsError500
from apiclient import UbidotsForbiddenError, UbidotsBulkOperationError, UbidotsInvalidInputError