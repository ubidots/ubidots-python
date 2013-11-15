import unittest
from ubidots.apiclient import ApiClient, UbidotsForbiddenError, UbidotsError404, UbidotsError400
from config import apikey, apikey2, base_url
from mock import patch, MagicMock, Mock
from contextlib import contextmanager



class TestCreationOfValues(unittest.TestCase):

    def setUp(self):
        self.NUMBER_OF_VALUES = 10
        # apikey = open('apikey.txt').readlines()[0]
        self.api = ApiClient(apikey, base_url = base_url)

        self.datasource = self.api.create_datasource({"name":"dstest01","description":"desc","tags":["dstest01", "01"]})
        self.variable = self.datasource.create_variable({"name":"vartest01", "unit":"C", "icon":"cloud"})


        for i in range(self.NUMBER_OF_VALUES):
            self.variable.save_value({"value":i})

    def tearDown(self):
        self.variable.remove_variable()
        self.datasource.remove_datasource()


    def test_can_read_values_from_a_variable(self):
        paginator = self.variable.get_values()
        values = paginator.get_all_items()
        self.assertEqual(len(values), self.NUMBER_OF_VALUES)


class TestDataSourcesEndPointNormalFlow(unittest.TestCase):

    def setUp(self):
        self.NUMBER_OF_DATASOURCES = 3
        self.NUMBER_OF_VARIABLES_PER_DS = 2
        self.api = ApiClient(apikey, base_url = base_url)

        self.ds_list = []
        self.var_list = []
        for datasource in range(self.NUMBER_OF_DATASOURCES):
            ds = self.api.create_datasource({"name":"dstest%s"%datasource})
            self.ds_list.append(ds)
            for variable in range(self.NUMBER_OF_VARIABLES_PER_DS):
                var = ds.create_variable({"name":"var%s"%variable, "unit":"c", "icon":"cloud"})
                self.var_list.append(var)

    def tearDown(self):
        [ds.remove_datasource() for ds in self.api.get_datasources().get_all_items()]



    ## Section list create datasources ##

    def test_detail_of_datasource_is_returned_when_created(self):
        newds = self.api.create_datasource({"name":"new_datasource"})
        self.assertTrue(hasattr(newds,'id'))


    def test_all_datasources_has_been_created_and_can_be_retrieved(self):
        ds_paginator = self.api.get_datasources()
        datasources = ds_paginator.get_all_items()
        self.assertEqual(len(datasources), self.NUMBER_OF_DATASOURCES)


    ## Section detail datasource ##

    def test_a_user_can_retrieve_one_datasource(self):
        datasource_id = self.ds_list[0].id
        ds = self.api.get_datasource(datasource_id)
        self.assertEqual(ds.id, self.ds_list[0].id)



    ### Section List Variables #####

    def test_all_user_variables_can_be_retrieved(self):
        var_paginator = self.api.get_variables()
        variables = var_paginator.get_all_items()
        self.assertEqual(len(variables), self.NUMBER_OF_DATASOURCES*self.NUMBER_OF_VARIABLES_PER_DS)



    ### Section Detail Variable ###

    def test_can_get_a_varible_detail(self):
        var_id = self.var_list[0].id
        variable = self.api.get_variable(var_id)
        self.assertEqual(variable.id, var_id)


    ### Section List Create Variables from Datasource ##

    def test_all_variables_has_been_created_and_can_be_retrievend_from_datasources(self):
        ds_paginator = self.api.get_datasources()
        datasources = ds_paginator.get_all_items()
        for datasource in datasources:
            variables = datasource.get_variables().get_all_items()
            self.assertEqual(len(variables), self.NUMBER_OF_VARIABLES_PER_DS)

    def test_detail_of_variable_is_returned_when_created(self):
        ds = self.ds_list[0]
        newvar = ds.create_variable({"name":"new_variable", "unit":"X", "icon":"cloud"})
        self.assertTrue(hasattr(newvar,'id'))

    ### Section Detail Variable from Datasource ##

    def test_can_access_a_variable_from_datasource(self):
        ds = self.ds_list[0]
        var_id = self.var_list[0].id
        newvar = ds.get_variable(var_id)
        self.assertEqual(newvar.id, var_id)


class TestDataSourcesEndPointErrors(unittest.TestCase):

    def setUp(self):
        self.api = ApiClient(apikey, base_url = base_url)

    def tearDown(self):
        [ds.remove_datasource() for ds in self.api.get_datasources().get_all_items()]

    @contextmanager
    def set_bad_token(self, api):
        token = api.bridge._token 
        api.bridge._token = "badtoken"
        api.bridge._set_token_header()
        api.bridge.initialize = Mock()

        yield api 

        api.bridge._token = token
        api.bridge._set_token_header()

    @contextmanager
    def set_other_user_enviroment(self, apikey2):
        api2 = ApiClient(apikey2, base_url = base_url)
        ds2 = api2.create_datasource({"name":"otherUserDs"})
        var2 = ds2.create_variable({"name":"othervar", "unit":"x", "icon":"cloud"})

        yield {"datasource":ds2, "variables":[var2]}

        datasources = api2.get_datasources().get_all_items()
        [ds.remove_datasource() for ds in datasources]



    def test_403_errors(self):
        ds = self.api.create_datasource({"name":"testds"})       
        with self.set_bad_token(self.api) as api:
            request_list =[
                {'method': api.get_datasources },
                {'method': api.create_datasource, 'args': [{"name":"bad_datasource"}] },
                {'method': api.get_variables },
                {'method': ds.get_variables},
                {'method': ds.create_variable, 'args':[{'name':'testvarname', 'unit':'x', 'icon':'cloud'}]},
            ]

            for request in request_list:
                self.assertRaises(UbidotsForbiddenError, request['method'], *request.get('args',[]) )


    ## Section detail datasource ##

    def test_a_user_cannot_retrieve_a_datasourse_of_other_user(self):
        with self.set_other_user_enviroment(apikey2) as otheruseritems:
            self.assertRaises(UbidotsForbiddenError, self.api.get_datasource, otheruseritems['datasource'].id)

    def test_a_mailformed_id_generates_a_400_error(self):
        self.assertRaises(UbidotsError400, self.api.get_datasource, "mailformedid")

    def test_api_raise_404_exception_if_datasource_does_not_exists(self):
        self.assertRaises(UbidotsError404, self.api.get_datasource, "000000000000000000000000")


    ## Section list variables ##
    def test_a_user_cannot_retrieve_a_variable_of_other_user(self):
        with self.set_other_user_enviroment(apikey2) as otheruseritems:
            self.assertRaises(UbidotsForbiddenError, self.api.get_variable, otheruseritems['variables'][0].id)






class TestDataSourceEndPointDeleteMethod(unittest.TestCase):

    def setUp(self):
        self.NUMBER_OF_DATASOURCES = 3
        self.NUMBER_OF_VARIABLES_PER_DS = 2
        self.api = ApiClient(apikey, base_url = base_url)

        self.ds_list = []
        for datasource in range(self.NUMBER_OF_DATASOURCES):
            ds = self.api.create_datasource({"name":"dstest%s"%datasource})
            self.ds_list.append(ds)
            for variable in range(self.NUMBER_OF_VARIABLES_PER_DS):
                ds.create_variable({"name":"var%s"%variable, "unit":"c", "icon":"cloud"})

    def tearDown(self):
        [ds.remove_datasource() for ds in self.api.get_datasources().get_all_items()]


    def test_datasources_and_variables_are_deleted_correctly(self):

        for datasource in self.ds_list:
            variables = datasource.get_variables().get_all_items()
            for variable in variables:
                variable.remove_variable()
            variables = datasource.get_variables().get_all_items()
            self.assertEqual(len(variables), 0)


        [ds.remove_datasource() for ds in self.ds_list]

        ds_paginator = self.api.get_datasources()
        datasources = ds_paginator.get_all_items()
        self.assertEqual(len(datasources), 0)
