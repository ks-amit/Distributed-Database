from . import models
import requests, json

INSERT_ADDR = '/api/user/insert'
GET_ADDR = '/api/user/get'
UPDATE_ADDR = '/api/user/update'

INSERT_BUS_SERVICE = '/api/bus/insert'

def get_database_name():
    queryset = models.DatabaseDetails.objects.exclude(name = 'primary').order_by('size')
    return queryset[0].name

def check_service_id(id):
    queryset = models.ServiceMetaData.objects.filter(id = id)
    if queryset.count() > 0:
        return False
    else:
        return True

def insert_bus_service(db_name, id, name, provider):
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + INSERT_BUS_SERVICE
    DATA = {'id': id, 'name': name}
    r = requests.post(db_addr, data = DATA)
    if r.status_code == 201:
        queryset.size += 1
        queryset.save()
        new_service = models.ServiceMetaData(id = id, name = name, type = 'B', db_name = db_name, provider = list([provider]))
        new_service.save()
    return r.status_code

def insert_user(db_name, email, password, token, type):
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + INSERT_ADDR
    DATA = {'email': email, 'password': password, 'token': token, 'type': type}
    r = requests.post(db_addr, data = DATA)
    if r.status_code == 201:    # NEW USER CREATED
        queryset.size += 1
        queryset.save()
        new_user = models.UserMetaData(email = email, db_name = db_name)
        new_user.save()
    return r.status_code

def get_user(db_name, email):
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + GET_ADDR
    DATA = {'email': email}
    r = requests.get(db_addr, data = DATA)
    return json.loads(r.text)[0]

def update_user(db_name, email, password = '', token = '', activated = '', type = ''):
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + UPDATE_ADDR
    DATA = {'email': email}
    if password != '':
        DATA.update({'password': password})
    if token != '':
        DATA.update({'token': token})
    if activated != '':
        DATA.update({'activated': activated})
    if type != '':
        DATA.update({'type': type})
    r = requests.post(db_addr, data = DATA)
    return r.status_code
