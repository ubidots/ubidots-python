import unittest
from ubidots.apiclient import ServerBridge
from ubidots.apiclient import try_again
from ubidots.apiclient import raise_informative_exception
from ubidots.apiclient import validate_input
from ubidots.apiclient import UbidotsError400, UbidotsError500, UbidotsInvalidInputError
from ubidots.apiclient import Paginator
from ubidots.apiclient import ApiObject
from ubidots.apiclient import Datasource
from ubidots.apiclient import ApiClient
from mock import patch, MagicMock, Mock, ANY
import json


class TestServerBridge(unittest.TestCase):

    def setUp(self):
        self.original_initialize = ServerBridge.initialize
        ServerBridge.initialize = MagicMock()
        apikey = "anyapikey"
        self.serverbridge = ServerBridge(apikey)
        self.serverbridge._token_header = {'X-AUTH-TOKEN': 'the token'}

    def tearDown(self):
        ServerBridge.initialize = self.original_initialize

    def test_when_ServerBridge_initializes_with_key_it_asks_for_a_token(self):
        with patch('ubidots.apiclient.requests') as mock_request:
            ServerBridge.initialize = self.original_initialize
            apikey = "anyapikey"
            sb = ServerBridge(apikey)
            mock_request.post.assert_called_once_with(
                "%s%s" % (sb.base_url, "auth/token"),
                headers={'content-type': 'application/json', 'X-UBIDOTS-APIKEY': 'anyapikey'}
            )

    def test_when_ServerBridge_initializes_with_token_it_set_it_correctly(self):
            sb = ServerBridge(token="anytoken")
            self.assertEqual(sb._token_header, {'X-AUTH-TOKEN': 'anytoken'})

    def test_get_includes_specific_headers(self):
        with patch('ubidots.apiclient.requests') as mock_request:
            self.serverbridge.get("any/path")

            mock_request.get.assert_called_once_with(
                "%s%s" % (self.serverbridge.base_url, "any/path"),
                headers={'content-type': 'application/json', 'X-AUTH-TOKEN': 'the token'}
            )

    def test_post_includes_specific_headers_and_data(self):
        with patch('ubidots.apiclient.requests') as mock_request:
            data = {"dataone": 1, "datatwo": 2}
            self.serverbridge.post("any/path", data)

            mock_request.post.assert_called_once_with(
                "%s%s" % (self.serverbridge.base_url, "any/path"),
                headers={'content-type': 'application/json', 'X-AUTH-TOKEN': 'the token'},
                data=json.dumps(data)
            )

    def test_delete_includes_specific_headers(self):
        with patch('ubidots.apiclient.requests') as mock_request:
            self.serverbridge.delete("any/path")

            mock_request.delete.assert_called_once_with(
                "%s%s" % (self.serverbridge.base_url, "any/path"),
                headers={'content-type': 'application/json', 'X-AUTH-TOKEN': 'the token'},
            )


class TestDecorators(unittest.TestCase):

    def test_try_again_decorator_number_of_tries_or_fail(self):
        from collections import namedtuple
        from ubidots.apiclient import UbidotsForbiddenError
        error_codes = [401]

        response = namedtuple('response', 'status_code')
        fn = Mock(side_effect=[response(error_codes[0]) for i in range(10)])
        real_decorator = try_again(error_codes, number_of_tries=10)

        serverbridge_mock = Mock()
        wrapper = real_decorator(fn)
        self.assertRaises(UbidotsForbiddenError, wrapper, serverbridge_mock)

    def test_raise_informative_exception_decorator(self):
        from collections import namedtuple
        error_codes = [400, 500]
        response = namedtuple('response', 'status_code')
        fn = Mock(side_effect=[response(error_codes[0]), response(error_codes[1])])
        real_decorator = raise_informative_exception(error_codes)
        wrapper = real_decorator(fn)
        self.assertRaises(UbidotsError400, wrapper, Mock())
        self.assertRaises(UbidotsError500, wrapper, Mock())

    def test_raise_validate_input_decorator_dict(self):
        real_decorator = validate_input(dict, ["a", "b", "c"])
        wrapper = real_decorator(lambda *args, **kwargs: 911)

        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), [])
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), {})
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), {"a": 1})
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), {"a": 1, "b": 1})
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), {"a": 1, "b": 1, "d": 1})

        self.assertEqual(wrapper(Mock(), {"a": 1, "b": 1, "c": 1}), 911)

    def test_raise_validate_input_decorator_list(self):
        real_decorator = validate_input(list, ["p", "q"])
        wrapper = real_decorator(lambda *args, **kwargs: 911)

        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), dict)
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), [{}])
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), [{"p"}])
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), [{"p": 1, "q": 1}, []])
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), [{"p": 1, "q": 1}, {}])
        self.assertRaises(UbidotsInvalidInputError, wrapper, Mock(), [{"p": 1, "q": 1}, {"p": 2}])

        self.assertEqual(wrapper(Mock(), [{"p": 1, "q": 1}]), 911)
        self.assertEqual(wrapper(Mock(), [{"p": 1, "q": 1}, {"p": 2, "q": 2}]), 911)

if __name__ == '__main__':
    unittest.main()


class TestPaginator(unittest.TestCase):

    def setUp(self):
        class fakebridge(object):
            pass

        def fake_transform_function(items, bridge):
            return [index for index, item in enumerate(items)]

        self.fakebridge = fakebridge
        self.fake_transform_function = fake_transform_function
        self.response = '{"count": 12, "next": null, "previous": "the/end/point/?page = 2", "results": [{"a":1},{"a":2},{"a":3},{"a":4},{"a":5}]}'
        self.response = json.loads(self.response)
        self.endpoint = "/the/end/point/"

    def test_paginator_calculates_number_of_items_per_page_and_number_of_pages(self):
        response = self.response
        pag = Paginator(self.fakebridge, response, self.fake_transform_function, self.endpoint)

        self.assertEqual(pag.items_per_page, 5)
        self.assertEqual(pag.number_of_pages, 3)

    def test_paginator_can_ask_for_a_specific_page(self):
        PAGE = 2
        response = self.response
        response_mock = Mock()
        response_mock.json = Mock(return_value=self.response)
        mock_bridge = Mock()
        mock_bridge.get = Mock(return_value=response_mock)
        pag = Paginator(mock_bridge, response, self.fake_transform_function, self.endpoint)
        response = pag.get_page(PAGE)

        mock_bridge.get.assert_called_once_with("%s?page=%s" % (self.endpoint, PAGE),)
        self.assertEqual(response, [0, 1, 2, 3, 4])

    def test_paginator_returns_exception_if_page_don_not_exist(self):
        pag = Paginator(self.fakebridge, self.response, self.fake_transform_function, self.endpoint)
        self.assertRaises(Exception, pag.get_page, (1000))

    def test_paginator_can_ask_for_the_last_x_values(self):
        pag = Paginator(self.fakebridge, self.response, self.fake_transform_function, self.endpoint)
        pag.get_pages = Mock()
        pag.items = {1: [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}, {"a": 5}], 2: [{"a": 6}, {"a": 7}, {"a": 8}, {"a": 9} , {"a": 10}], 3: [{"a" :11}, {"a": 12}]}
        values = pag.get_last_items(7)
        self.assertEqual(values,[{"a":1},{"a":2},{"a":3},{"a":4},{"a":5}, {"a":6}, {"a":7}] )

    def test_paginator_can_ask_for_all_the_items(self):
        pag = Paginator(self.fakebridge, self.response, self.fake_transform_function, self.endpoint)
        pag.get_pages = Mock()
        pag.items = {1:[{"a":1},{"a":2},{"a":3},{"a":4},{"a":5}], 2:[{"a":6},{"a":7},{"a":8},{"a":9},{"a":10}], 3:[{"a":11},{"a":12}]}
        values = pag.get_all_items()
        self.assertEqual(values,[{"a":1},{"a":2},{"a":3},{"a":4},{"a":5}, {"a":6}, {"a":7},{"a":8},{"a":9},{"a":10},{"a":11},{"a":12}] )


    def test_paginator_can_ask_for_the_range_of_pages(self):
        response = self.response
        pag = Paginator(self.fakebridge, response, self.fake_transform_function, self.endpoint)
        self.assertEqual(pag.pages, [1,2,3])


    def test_paginator_make_the_custom_transformation(self):

        class fakebridge(object):
            pass

        def transformation_function(items, bridge):
            for item in items:
                item['a'] = item['a'] + 1
            return items


        any_dict = '{"count": 4, "next": null, "previous": null, "results": [{"a":1},{"a":2},{"a":3},{"a":4}]}'
        any_dict = json.loads(any_dict)
        pag = Paginator(fakebridge,any_dict,transformation_function, self.endpoint)


class TestApiObject(unittest.TestCase):

    def test_init_method_transfrom_raw_dictionary_items_to_object_attribute(self):
        raw_data = {'key1':'val1','key2':'val2'}
        bridge = Mock()
        newapiobject = ApiObject(raw_data, bridge)

        self.assertEqual(newapiobject.key1, 'val1')
        self.assertEqual(newapiobject.key2, 'val2')


class TestDatasource(unittest.TestCase):

    def test_method_get_variables_make_a_request_to_an_specific_endpoint(self):
        ds_id = 'any_id'
        endpoint = 'datasources/' + ds_id + '/variables'
        raw_ds = {"id": ds_id, "name":"testds", "tags":['a', 'b', 'c'], "description":"the description"}
        bridge = Mock()
        ds = Datasource(raw_ds, bridge)
        ds.get_new_paginator = Mock()
        ds.get_variables()
        bridge.get.assert_called_once_with(endpoint)

    def test_method_get_variables_make_a_request_to_an_specific_endpoint(self):
        ds_id = 'any_id'
        endpoint = 'datasources/' + ds_id + '/variables'
        raw_ds = {"id": ds_id, "name":"testds", "tags":['a', 'b', 'c'], "description":"the description"}
        bridge = Mock()
        ds = Datasource(raw_ds, bridge)
        ds.get_new_paginator = Mock()
        ds.get_variables()
        ds.get_new_paginator.assert_called_once_with(bridge, ANY, ANY, endpoint)


class TestVariables(unittest.TestCase):
    pass


class TestApiClient(unittest.TestCase):

    def test_if_bridge_is_provided_other_arguments_are_not_needed(self):
        bridge = Mock()
        api = ApiClient(bridge=bridge)
        self.assertEqual(api.bridge, bridge)
