from . import models
import requests, json

INSERT_ADDR = '/api/user/insert'
GET_ADDR = '/api/user/get'
UPDATE_ADDR = '/api/user/update'

INSERT_BUS_SERVICE = '/api/bus/insert'
DELETE_BUS_SERVICE = '/api/bus/delete'
GET_BUS_SERVICE = '/api/bus/list/email'
UPDATE_BUS_SERVICE = '/api/bus/update'
GET_BUS_SERVICE_ID = '/api/bus/get'

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
    DATA = {'id': id, 'name': name, 'provider': provider}
    r = requests.post(db_addr, data = DATA)
    if r.status_code == 201:
        queryset.size += 1
        queryset.save()
        new_service = models.ServiceMetaData(id = id, name = name, type = 'B', db_name = db_name, provider = list([provider]))
        new_service.save()
    return r.status_code

def get_bus_service_by_email(email):
    queryset = models.DatabaseDetails.objects.exclude(name = 'primary')
    services = []
    for db in queryset:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_SERVICE
            DATA = {'email': email}
            r = requests.post(db_addr, data = DATA)
            S = json.loads(r.text)
            services += S
        except Exception as e:
            print('EXCEPTION ', db.port)
            print(e)
            continue
    return services

def get_bus_service_by_id(id):
    metaData = models.ServiceMetaData.objects.filter(id = id)
    metaData = metaData[0]
    db_name = metaData.db_name
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + GET_BUS_SERVICE_ID
    DATA = {'id': id}
    r = requests.get(db_addr, data = DATA)
    return json.loads(r.text)[0]

def update_bus_service(id, name = None, price = None, bus_number = None, is_ready = None, seats = None, provider = None, route = None, timing = None, provider_code = None, route_code = None, timing_code = None):
    metaData = models.ServiceMetaData.objects.filter(id = id)
    metaData = metaData[0]
    db_name = metaData.db_name
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + UPDATE_BUS_SERVICE
    DATA = {'id': id}
    if name != None:
        DATA.update({'name': name})
    if price != None:
        DATA.update({'price': int(price)})
    if bus_number != None:
        DATA.update({'bus_number': bus_number})
    if is_ready != None:
        DATA.update({'is_ready': is_ready})
    if seats != None:
        DATA.update({'seats': seats})
    if provider != None:
        DATA.update({'provider': provider})
    if route != None:
        DATA.update({'route': route})
    if timing != None:
        DATA.update({'timing': timing})
    if provider_code != None:
        DATA.update({'provider_code': provider_code})
    if route_code != None:
        DATA.update({'route_code': route_code})
    if timing_code != None:
        DATA.update({'timing_code': timing_code})
    r = requests.post(db_addr, data = DATA)
    return r.status_code

def delete_bus_service(id):
    metaData = models.ServiceMetaData.objects.filter(id = id)
    metaData = metaData[0]
    db_name = metaData.db_name
    queryset = models.DatabaseDetails.objects.filter(name = db_name)[0]
    db_addr = 'http://' + queryset.ip_addr + ':' + queryset.port + DELETE_BUS_SERVICE
    DATA = {'id': id}
    r = requests.post(db_addr, data = DATA)
    if r.status_code == 200:
        queryset.size -= 1
        queryset.save()
        metaData.delete()
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

def get_user_by_email(email):
    metaData = models.UserMetaData.objects.filter(email = email)
    metaData = metaData[0]
    db_name = metaData.db_name
    return get_user(db_name, email)

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
