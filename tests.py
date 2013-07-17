from apiclient import ApiClient

apikey = None
with open('apikey.txt') as f:
	apikey =  f.readline()

api = ApiClient(apikey)

################################CREACIONES ##################################################

# #Se puede crear un datasource
# print api.create_datasource({'name':'deletethis'})


# #se puede crear una variable desde un datasource
# ds = api.create_datasource({'name':'deletethis'})
# print ds.create_variable({'name':'vardeletethis', 'unit':'C'})

##########################################DATASOURCES  ###############################################

# # #Puedo Listar Datasources
# lista_datasources = api.datasources()
# print lista_datasources

# # #Puedo traer un datasource especifico por key
# ds_especifico = api.datasource("51a7b273f91b280d044d8572")
# print ds_especifico

# #puedo traer un datasource especifico por url:
# ds_especifico = api.datasource(url = "http://app.ubidots.com/api/datasources/51a7b273f91b280d044d8572")
# print ds_especifico



##############################VARIABLES ######################################################

# ds = api.datasource(url = "http://app.ubidots.com/api/datasources/51bb3281f91b2857e9a84cec")

# #de un datasource puedo listar todas sus variables
# print ds.variables()

# #desde el api puedo recibir una variable si tengo su id
# print api.variable("51bb6cbaf91b28585e24305c")

# #desde una variable se puede tener acceso al datasource
# print api.variable("51bb6cbaf91b28585e24305c").datasource



###############################Valores de variables ##################################

# variable = api.variable("51bb6cbaf91b28585e24305c")


# #Desde una variable se puede tener acceso a los valores #
# print len(variable.values())


# #Se puede postear un dato en una variable
# ds = api.create_datasource({'name':'deletethis'})
# var =  ds.create_variable({'name':'vardeletethis', 'unit':'C'})
# import random
# for i in range(10):
# 	var.save_value({'value':random.randint(1,10)})

#######################################DELETE DATASOURCE ##############################################

# ds = api.create_datasource({'name':'deletethis'})
# print ds
# print ds.remove() 

###############################DELETE VARIABLES ########################################################
# ds = api.create_datasource({'name':'deletethis'})
# var  = ds.create_variable({'name':'vardeletethis', 'unit':'C'})
# print var.remove()


#######################################Scripts para borrar datasources creados####################################
# ds_list = api.datasources()

# for ds in ds_list:
# 	if ds.name == 'deletethis':
# 		ds.remove()
