from . import models
import requests, json
from django.db.models import F
from urllib.parse import quote, unquote

replication_factor = 3

STATUS = '/api/status'

INSERT_ADDR = '/api/user/insert'
GET_ADDR = '/api/user/get'
UPDATE_ADDR = '/api/user/update'

INSERT_BUS_SERVICE = '/api/bus/insert'
DELETE_BUS_SERVICE = '/api/bus/delete'
GET_BUS_SERVICE = '/api/bus/list/email'
UPDATE_BUS_SERVICE = '/api/bus/update'
GET_BUS_SERVICE_ID = '/api/bus/get'

INSERT_HOTEL_SERVICE = '/api/hotels/insert'
UPDATE_HOTEL_SERVICE = '/api/hotels/update'
GET_HOTEL_SERVICE_ID = '/api/hotels/get'
DELETE_HOTEL_SERVICE = '/api/hotels/delete'
GET_HOTEL_SERVICE = '/api/hotels/list/email'
GET_HOTEL_SERVICE_BY_CITY = '/api/hotels/list/city'

HOTEL_BOOKING = '/api/bookings/hotel/new'
GET_HOTEL_BOOKING_BY_HOTEL = '/api/bookings/hotel/get'
GET_HOTEL_BOOKING_BY_USER = '/api/bookings/hotel/user'
GET_HOTEL_BOOKING_BY_ID = '/api/bookings/hotel/id'
DELETE_HOTEL_BOOKING = '/api/bookings/hotel/delete'
GET_HOTEL_BOOKING_BY_DATE = '/api/bookings/hotel/date'

BUS_BOOKING = '/api/bookings/bus/new'
GET_BUS_SERVICE_BY_CITY = '/api/bus/list/city'
GET_BUS_BOOKING_BY_BUS = '/api/bookings/bus/get'
GET_BUS_BOOKING_BY_ID = '/api/bookings/bus/id'
DELETE_BUS_BOOKING = '/api/bookings/bus/delete'
GET_BUS_BOOKING_BY_USER = '/api/bookings/bus/user'
GET_BUS_BOOKING_BY_DATE = '/api/bookings/bus/date'

########################### REPLICATION HELPERS ########################

def get_3_databases():
    queryset = models.DatabaseDetails.objects.filter(status = '1').exclude(name = 'primary').order_by('size')
    return queryset[:3]


def check_primary(metaData):
    primary = models.DatabaseDetails.objects.get(name = metaData.db_name_0)
    db1 = models.DatabaseDetails.objects.get(name = metaData.db_name_1)
    db2 = models.DatabaseDetails.objects.get(name = metaData.db_name_2)
    if primary.status == '0':
        if db1.status == '1':
            metaData.db_name_0 = db1.name
            metaData.db_name_1 = primary.name
        elif db2.status == '1':
            metaData.db_name_0 = db2.name
            metaData.db_name_2 = primary.name
        metaData.save()

def encode_dict(D):
    D1 = [ [], [] ]
    D2 = [ [], [] ]
    D3 = [ [], [] ]
    D4 = [ [], [] ]
    D5 = [ [], [] ]
    for item in D:
        value = D[item]
        T = type(value).__name__
        if T == 'str':
            D1[0].append(item)
            D1[1].append(value)
        elif T == 'int':
            D5[0].append(item)
            D5[1].append(value)
        elif T == 'time':
            D2[0].append(item)
            D2[1].append(value)
        elif T == 'date':
            D3[0].append(item)
            D3[1].append(value)
        elif T == 'bool':
            D4[0].append(item)
            D4[1].append(value)

    return D1, D2, D3, D4, D5

def make_dict(update):
    D11 = update.data_string_keys
    D12 = update.data_string_values
    D21 = update.data_time_keys
    D22 = update.data_time_values
    D31 = update.data_date_keys
    D32 = update.data_date_values
    D41 = update.data_boolean_keys
    D42 = update.data_boolean_values
    D51 = update.data_int_keys
    D52 = update.data_int_values

    D = {}

    for i in range(len(D11)):
        D[D11[i]] = D12[i]

    for i in range(len(D21)):
        D[D21[i]] = D22[i]

    for i in range(len(D31)):
        D[D31[i]] = D32[i]

    for i in range(len(D41)):
        D[D41[i]] = D42[i]

    for i in range(len(D51)):
        D[D51[i]] = D52[i]

    return D

def handle_update_status(DATA, UP, type, db_names):
    db_addr_1 = DATA.get('db_addr_1')
    db_addr_2 = DATA.get('db_addr_2')
    del DATA['db_addr_1']
    del DATA['db_addr_2']
    D1, D2, D3, D4, D5 = encode_dict(DATA)
    if UP.get('db_addr_1') == False:
        pending_update = models.PendingUpdates( data_string_keys = D1[0], data_string_values = D1[1],
                                                data_time_keys = D2[0], data_time_values = D2[1],
                                                data_date_keys = D3[0], data_date_values = D3[1],
                                                data_boolean_keys = D4[0], data_boolean_values = D4[1],
                                                data_int_keys = D5[0], data_int_values = D5[1],
                                                addr = db_addr_1, type = type, db_name = db_names['db_addr_1'])
        pending_update.save()
    if UP.get('db_addr_2') == False:
        pending_update = models.PendingUpdates( data_string_keys = D1[0], data_string_values = D1[1],
                                                data_time_keys = D2[0], data_time_values = D2[1],
                                                data_date_keys = D3[0], data_date_values = D3[1],
                                                data_boolean_keys = D4[0], data_boolean_values = D4[1],
                                                data_int_keys = D5[0], data_int_values = D5[1],
                                                addr = db_addr_2, type = type, db_name = db_names['db_addr_2'])
        pending_update.save()

def perform_update(update):
    DATA = make_dict(update)
    db_addr = update.addr
    type = update.type
    try:
        if type == 'POST':
            r = requests.post(db_addr, data = DATA)
        elif type == 'PUT':
            r = requests.put(db_addr, data = DATA)
        elif type == 'GET':
            r = requests.get(db_addr, data = DATA)
        return r.status_code
    except Exception as e:
        print(e)
        return 400


#######################################################################

def get_travel_time(T1, T2):
    T1 = T1.split(':')
    T2 = T2.split(':')
    day1 = int(T1[0])
    day2 = int(T2[0])
    hour1 = int(T1[1])
    hour2 = int(T2[1])
    min1 = int(T1[2])
    min2 = int(T2[2])
    travel_time = (day2 - day1) * (24 * 60)
    travel_time += (hour2 - hour1) * 60
    travel_time += (min2 - min1)
    return travel_time

def check_status():
    D = {'primary': 1}
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + STATUS
            r = requests.get(db_addr)
            if r.status_code == 200:
                D[db.name] = 1
            else:
                D[db.name] = 0
        except Exception as e:
            D[db.name] = 0
            continue

    return D

def update_database_status():
    S = check_status()
    for key in S:
        db = models.DatabaseDetails.objects.get(name = key)
        db.status = S[key]
        db.save()

def check_booking_id(id):
    queryset = models.BookingMetaData.objects.filter(id = id)
    if queryset.count() > 0:
        return False
    else:
        return True

def check_service_id(id):
    queryset = models.ServiceMetaData.objects.filter(id = id)
    if queryset.count() > 0:
        return False
    else:
        return True

########################## REP VERSION #######################

def get_hotel_booking_by_date_rep(id, date):

        dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
        DATA = {'id': id, 'date': date}
        D = {}
        bookings = []
        for db in dbs:

            try:

                db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_BOOKING_BY_DATE
                r = requests.post(db_addr, data = DATA)
                B = json.loads(r.text)
                for booking in B:
                    b_id = booking.get('id')
                    if b_id not in D:
                        D[b_id] = 1
                        bookings.append(booking)

            except Exception as e:
                continue

        return bookings

def get_hotel_booking_by_id_rep(id):

    metaData = models.BookingMetaData.objects.get(id = id)
    check_primary(metaData)
    for i in range(3):

        try:

            db_name = 'db_name_' + str(i)
            db = models.DatabaseDetails.objects.get(name = getattr(metaData, db_name))
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_BOOKING_BY_ID + '/' + quote(id)
            r = requests.get(db_addr)
            return json.loads(r.text)[0]

        except:
            continue

def delete_hotel_booking_rep(id):

    try:

        metaData = models.BookingMetaData.objects.get(id = id)
        check_primary(metaData)

        primary = models.DatabaseDetails.objects.get(name = metaData.db_name_0)
        sec1 = models.DatabaseDetails.objects.get(name = metaData.db_name_1)
        sec2 = models.DatabaseDetails.objects.get(name = metaData.db_name_2)

        db_addr_0 = 'http://' + primary.ip_addr + ':' + primary.port + DELETE_HOTEL_BOOKING
        db_addr_1 = 'http://' + sec1.ip_addr + ':' + sec1.port + DELETE_HOTEL_BOOKING
        db_addr_2 = 'http://' + sec2.ip_addr + ':' + sec2.port + DELETE_HOTEL_BOOKING

        db_names = {'db_addr_1': sec1.name, 'db_addr_2': sec2.name}

        DATA = {'id': id}
        DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})

        r = requests.post(db_addr_0, data = DATA)

        print(r.text)

        if r.status_code == 200:

            primary.size -= 4
            sec1.size -= 4
            sec2.size -= 4
            primary.save()
            sec1.save()
            sec2.save()
            metaData.delete()
            UP = json.loads(r.text)
            print(UP)
            handle_update_status(DATA, UP, 'POST', db_names)

        return r.status_code

    except Exception as e:
        print(e)
        return 400

##############################################################

def get_hotel_booking_by_user(email):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    A = []
    D = {}
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_BOOKING_BY_USER + '/' + quote(email)
            r = requests.get(db_addr)
            S = json.loads(r.text)
            for dic in S:
                if dic.get('id') not in D:
                    A.append(dic)
                    D[dic.get('id')] = 1
        except:
            continue

    return A

####################### REP VERSION ##########################

def new_hotel_booking_rep(id, service_id, email, in_date, out_date, booking_date, rooms, bill):

    dbs = models.DatabaseDetails.objects.exclude(name = 'primary').filter(status = '1').order_by('size')
    counter = 0
    DATA = {'id': id, 'service_id': service_id, 'email': email, 'in_date': in_date, 'out_date': out_date, 'booking_date': booking_date, 'rooms': rooms, 'bill': bill}
    db_names = []
    for db in dbs:

        try:

            db_addr = 'http://' + db.ip_addr + ':' + db.port + HOTEL_BOOKING
            r = requests.post(db_addr, data = DATA)
            if r.status_code == 201:
                db_names.append(db.name)
                counter += 1
                db.size += 4
                db.save()

                if counter == replication_factor:
                    break

        except:
            continue

    if counter == replication_factor:
        new_booking = models.BookingMetaData(id = id, type = 'H', db_name_0 = db_names[0], db_name_1 = db_names[1], db_name_2 = db_names[2], start_date = in_date)
        new_booking.db_name = db_names[0]       # remove later
        new_booking.save()
        return 201

    return 201


##############################################################

def get_hotel_bookings_by_hotel(service_id, in_date, out_date):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    D = {}
    counter = 0
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_BOOKING_BY_HOTEL
            print(db_addr)
            DATA = {'service_id': service_id, 'in_date': in_date, 'out_date': out_date}
            r = requests.post(db_addr, data = DATA)
            S = json.loads(r.text)
            for dic in S:
                if dic.get('id') not in D:
                    D[dic.get('id')] = 1
                    counter += dic.get('rooms')
        except:
            continue

    return counter

def get_hotel_services_city(city, area = None):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    D = {}
    A = []
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_SERVICE_BY_CITY
            if area == None:
                DATA = {'city': city.upper()}
            else:
                DATA = {'city': city.upper(), 'area': area.upper()}
            r = requests.post(db_addr, data = DATA)
            S = json.loads(r.text)
            for dic in S:
                if dic.get('id') not in D:
                    D[dic.get('id')] = 1
                    A.append(dic)
        except:
            continue

    return A

####################### REP VERSION ###########################

def insert_bus_service_rep(id, name, provider):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary').filter(status = '1').order_by('size')
    counter = 0
    db_names = ['' for i in range(replication_factor)]
    for db in dbs:
        db_addr = 'http://' + db.ip_addr + ':' + db.port + INSERT_BUS_SERVICE
        DATA = {'id': id, 'name': name, 'provider': provider}
        r = requests.post(db_addr, data = DATA)
        if r.status_code == 201:
            db.size += 17
            db.save()
            counter += 1
            db_names[counter - 1] = db.name
            if counter == replication_factor:
                break

    new_bus = models.ServiceMetaData(id = id, name = name, type = 'B', db_name_0 = db_names[0], db_name_1 = db_names[1], db_name_2 = db_names[2], provider = list([provider]))
    new_bus.db_name = db_names[0]              # COMMENT LATER
    new_bus.save()

    if counter == replication_factor:
        return 201
    else:
        return 404

def insert_hotel_service_rep(id, name, provider):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary').filter(status = '1').order_by('size')
    counter = 0
    db_names = ['' for i in range(replication_factor)]
    for db in dbs:
        db_addr = 'http://' + db.ip_addr + ':' + db.port + INSERT_HOTEL_SERVICE
        DATA = {'id': id, 'name': name, 'provider': provider}
        r = requests.post(db_addr, data = DATA)
        if r.status_code == 201:
            db.size += 18
            db.save()
            counter += 1
            db_names[counter - 1] = db.name
            if counter == replication_factor:
                break

    new_hotel = models.ServiceMetaData(id = id, name = name, type = 'H', db_name_0 = db_names[0], db_name_1 = db_names[1], db_name_2 = db_names[2], provider = list([provider]))
    new_hotel.db_name = db_names[0]              # COMMENT LATER
    new_hotel.save()

    if counter == replication_factor:
        return 201
    else:
        return 404

###########################################################

###################### REP VERSION ########################################

def update_hotel_service_rep(id, name = None, price = None, city = None, area = None, is_ready = None, address = None, description = None, rooms = None, provider = None, check_in = None, check_out = None, provider_code = None):
    metaData = models.ServiceMetaData.objects.get(id = id)
    check_primary(metaData)
    primary = metaData.db_name_0
    sec1 = metaData.db_name_1
    sec2 = metaData.db_name_2

    db = models.DatabaseDetails.objects.get(name = primary)
    db1 = models.DatabaseDetails.objects.get(name = sec1)
    db2 = models.DatabaseDetails.objects.get(name = sec2)

    db_addr_0 = 'http://' + db.ip_addr + ':' + db.port + UPDATE_HOTEL_SERVICE
    db_addr_1 = 'http://' + db1.ip_addr + ':' + db1.port + UPDATE_HOTEL_SERVICE
    db_addr_2 = 'http://' + db2.ip_addr + ':' + db2.port + UPDATE_HOTEL_SERVICE
    db_name_0 = db.name
    db_name_1 = db1.name
    db_name_2 = db2.name
    db_names = {'db_addr_1': db_name_1, 'db_addr_2': db_name_2}

    DATA = {'id': id}
    if name != None:
        DATA.update({'name': name})
    if price != None:
        DATA.update({'price': int(price)})
    if address != None:
        DATA.update({'address': address})
    if city != None:
        DATA.update({'city': city.upper()})
    if area != None:
        DATA.update({'area': area.upper()})
    if description != None:
        DATA.update({'description': description})
    if is_ready != None:
        DATA.update({'is_ready': is_ready})
    if rooms != None:
        DATA.update({'rooms': rooms})
    if provider != None:
        DATA.update({'provider': provider})
    if check_in != None:
        DATA.update({'check_in': check_in})
    if check_out != None:
        DATA.update({'check_out': check_out})
    if provider_code != None:
        DATA.update({'provider_code': provider_code})

    DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})
    try:
        r = requests.post(db_addr_0, data = DATA)
        UP = json.loads(r.text)
        handle_update_status(DATA, UP, 'POST', db_names)
        return r.status_code
    except Exception as e:
        print(e)
        return 400

##########################################################################

###################### REP VERSION ##################################

def get_services_by_email_rep(email):
    metaData = models.ServiceMetaData.objects.filter(provider__contains = [email])
    bus_services = []
    hotel_services = []
    for service in metaData:
        S = get_service_by_id_rep(service.id)
        if service.id[0] == 'B':
            bus_services.append(S)
        else:
            hotel_services.append(S)

    return bus_services, hotel_services

def get_service_by_id_rep(id):
    if id[0] == 'H':
        return get_hotel_service_by_id_rep(id)
    if id[0] == 'B':
        return get_bus_service_by_id_rep(id)

def get_hotel_service_by_id_rep(id):
    metaData = models.ServiceMetaData.objects.get(id = id)
    check_primary(metaData)
    for i in range(3):
        try:
            db_name = 'db_name_' + str(i)
            db = models.DatabaseDetails.objects.get(name = getattr(metaData, db_name))
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_SERVICE_ID
            DATA = {'id': id}
            r = requests.get(db_addr, data = DATA)
            return json.loads(r.text)[0]
        except:
            print('SKIPPED: ', db_name)
            continue

###########################################################################

# def get_hotel_service_by_email(email):
#     queryset = models.DatabaseDetails.objects.exclude(name = 'primary')
#     services = []
#     for db in queryset:
#         try:
#             db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_HOTEL_SERVICE
#             DATA = {'email': email}
#             r = requests.post(db_addr, data = DATA)
#             S = json.loads(r.text)
#             services += S
#         except Exception as e:
#             print('EXCEPTION ', db.port)
#             print(e)
#             continue
#     return services

############################### REP VERSION ##############################

def delete_hotel_service_rep(id):

    try:

        metaData = models.ServiceMetaData.objects.get(id = id)

        check_primary(metaData)

        primary = models.DatabaseDetails.objects.get(name = metaData.db_name_0)
        sec1 = models.DatabaseDetails.objects.get(name = metaData.db_name_1)
        sec2 = models.DatabaseDetails.objects.get(name = metaData.db_name_2)

        db_addr_0 = 'http://' + primary.ip_addr + ':' + primary.port + DELETE_HOTEL_SERVICE
        db_addr_1 = 'http://' + sec1.ip_addr + ':' + sec1.port + DELETE_HOTEL_SERVICE
        db_addr_2 = 'http://' + sec2.ip_addr + ':' + sec2.port + DELETE_HOTEL_SERVICE

        db_names = {'db_addr_1': sec1.name, 'db_addr_2': sec2.name}

        DATA = {'id': id}

        DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})

        r = requests.post(db_addr_0, data = DATA)

        if r.status_code == 200:

            primary.size -= 18
            sec1.size -= 18
            sec2.size -= 18
            primary.save()
            sec1.save()
            sec2.save()
            metaData.delete()
            UP = json.loads(r.text)
            handle_update_status(DATA, UP, 'POST', db_names)

        return r.status_code

    except Exception as e:
        print(e)
        return 400

##########################################################################

# def get_bus_service_by_email(email):
#     queryset = models.DatabaseDetails.objects.exclude(name = 'primary')
#     services = []
#     for db in queryset:
#         try:
#             db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_SERVICE
#             DATA = {'email': email}
#             r = requests.post(db_addr, data = DATA)
#             S = json.loads(r.text)
#             services += S
#         except Exception as e:
#             print('EXCEPTION ', db.port)
#             print(e)
#             continue
#     return services

################################## REP VERSION ################################

def get_bus_service_by_id_rep(id):
    metaData = models.ServiceMetaData.objects.get(id = id)
    check_primary(metaData)
    for i in range(3):
        try:
            db_name = 'db_name_' + str(i)
            db = models.DatabaseDetails.objects.get(name = getattr(metaData, db_name))
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_SERVICE_ID
            DATA = {'id': id}
            r = requests.get(db_addr, data = DATA)
            return json.loads(r.text)[0]
        except:
            continue

def update_bus_service_rep(id, name = None, price = None, bus_number = None, is_ready = None, seats = None, provider = None, route = None, timing = None, boarding_point = None, provider_code = None, route_code = None, timing_code = None, boarding_code = None):

    try:

        metaData = models.ServiceMetaData.objects.get(id = id)

        check_primary(metaData)

        primary = models.DatabaseDetails.objects.get(name = metaData.db_name_0)
        sec1 = models.DatabaseDetails.objects.get(name = metaData.db_name_1)
        sec2 = models.DatabaseDetails.objects.get(name = metaData.db_name_2)

        db_addr_0 = 'http://' + primary.ip_addr + ':' + primary.port + UPDATE_BUS_SERVICE
        db_addr_1 = 'http://' + sec1.ip_addr + ':' + sec1.port + UPDATE_BUS_SERVICE
        db_addr_2 = 'http://' + sec2.ip_addr + ':' + sec2.port + UPDATE_BUS_SERVICE

        db_names = {'db_addr_1': sec1.name, 'db_addr_2': sec2.name}

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
        if boarding_point != None:
            if boarding_code != 'REMOVE':
                DATA.update({'boarding_point': boarding_point.upper()})
            else:
                DATA.update({'boarding_point': boarding_point})
        if route != None:
            if route_code != 'REMOVE':
                DATA.update({'route': route.upper()})
            else:
                DATA.update({'route': route})
        if timing != None:
            DATA.update({'timing': timing})
        if provider_code != None:
            DATA.update({'provider_code': provider_code})
        if route_code != None:
            DATA.update({'route_code': route_code})
        if timing_code != None:
            DATA.update({'timing_code': timing_code})
        if boarding_code != None:
            DATA.update({'boarding_code': boarding_code})

        DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})

        r = requests.post(db_addr_0, data = DATA)

        UP = json.loads(r.text)
        handle_update_status(DATA, UP, 'POST', db_names)
        return r.status_code

    except Exception as e:
        print(e)
        return 400

###############################################################################

######################## REP VERSION ##############################

def delete_bus_service_rep(id):

    try:

        metaData = models.ServiceMetaData.objects.get(id = id)
        check_primary(metaData)

        primary = models.DatabaseDetails.objects.get(name = metaData.db_name_0)
        sec1 = models.DatabaseDetails.objects.get(name = metaData.db_name_1)
        sec2 = models.DatabaseDetails.objects.get(name = metaData.db_name_2)

        db_addr_0 = 'http://' + primary.ip_addr + ':' + primary.port + DELETE_BUS_SERVICE
        db_addr_1 = 'http://' + sec1.ip_addr + ':' + sec1.port + DELETE_BUS_SERVICE
        db_addr_2 = 'http://' + sec2.ip_addr + ':' + sec2.port + DELETE_BUS_SERVICE

        db_names = {'db_addr_1': sec1.name, 'db_addr_2': sec2.name}

        DATA = {'id': id}
        DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})

        r = requests.post(db_addr_0, data = DATA)

        if r.status_code == 200:

            primary.size -= 18
            sec1.size -= 18
            sec2.size -= 18
            primary.save()
            sec1.save()
            sec2.save()
            metaData.delete()
            UP = json.loads(r.text)
            handle_update_status(DATA, UP, 'POST', db_names)

        return r.status_code

    except Exception as e:
        print(e)
        return 400

def insert_user(email, password, token, type):
    queryset = models.DatabaseDetails.objects.filter(status = '1').exclude(name = 'primary').order_by('size')
    counter = 0
    db_names = ['' for i in range(replication_factor)]
    for db in queryset:

        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + INSERT_ADDR
            DATA = {'email': email, 'password': password, 'token': token, 'type': type}
            r = requests.post(db_addr, data = DATA)
            if r.status_code == 201:
                db.size += 5
                db.save()
                counter += 1
                db_names[counter - 1] = db.name
                if counter == replication_factor:
                    break

        except Exception as e:
            continue

    if counter == replication_factor:
        new_user = models.UserMetaData(email = email, db_name_0 = db_names[0], db_name_1 = db_names[1], db_name_2 = db_names[2])
        new_user.save()
        return 201
    else:
        return 404

def get_user_by_email(email):
    metaData = models.UserMetaData.objects.filter(email = email)
    metaData = metaData[0]
    return get_user_rep(metaData)

############ REP VERSION #################

def get_user_rep(user):
    check_primary(user)
    db = models.DatabaseDetails.objects.get(name = user.db_name_0)
    if db.status == '1':
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_ADDR
            DATA = {'email': user.email}
            r = requests.get(db_addr, data = DATA)
            return json.loads(r.text)[0]
        except:
            pass

    db = models.DatabaseDetails.objects.get(name = user.db_name_1)
    if db.status == '1':
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_ADDR
            DATA = {'email': user.email}
            r = requests.get(db_addr, data = DATA)
            return json.loads(r.text)[0]
        except:
            pass

    db = models.DatabaseDetails.objects.get(name = user.db_name_2)
    if db.status == '1':
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_ADDR
            DATA = {'email': user.email}
            r = requests.get(db_addr, data = DATA)
            return json.loads(r.text)[0]
        except:
            pass

    return 404

#########################################################################

####################### REP VERSION ########################

def update_user_rep(user, password = '', token = '', activated = '', type = ''):
    check_primary(user)
    primary = models.DatabaseDetails.objects.get(name = user.db_name_0)
    sec1 = models.DatabaseDetails.objects.get(name = user.db_name_1)
    sec2 = models.DatabaseDetails.objects.get(name = user.db_name_2)

    db_addr_0 = 'http://' + primary.ip_addr + ':' + primary.port + UPDATE_ADDR
    db_addr_1 = 'http://' + sec1.ip_addr + ':' + sec1.port + UPDATE_ADDR
    db_addr_2 = 'http://' + sec2.ip_addr + ':' + sec2.port + UPDATE_ADDR

    db_names = {'db_addr_1': sec1.name, 'db_addr_2': sec2.name}

    try:

        DATA = {'email': user.email}
        if password != '':
            DATA.update({'password': password})
        if token != '':
            DATA.update({'token': token})
        if activated != '':
            DATA.update({'activated': activated})
        if type != '':
            DATA.update({'type': type})

        DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})

        r = requests.post(db_addr_0, data = DATA)
        UP = json.loads(r.text)
        handle_update_status(DATA, UP, 'POST', db_names)

        return r.status_code

    except Exception as e:
        print(e)
        return 400


#########################################################################################

def get_bus_services_city(From, To):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    D = {}
    A = []
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_SERVICE_BY_CITY
            DATA = {'From': From.upper(), 'To': To.upper() }
            r = requests.post(db_addr, data = DATA)
            S = json.loads(r.text)
            for dic in S:
                if dic.get('id') not in D:
                    D[dic.get('id')] = 1
                    A.append(dic)
        except Exception as e:
            print(e)
            continue

    return A

def get_bus_bookings_by_bus(service_id, From, To, TravelDate):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    D = {}
    counter = 0
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_BOOKING_BY_BUS
            print(db_addr)
            DATA = {'service_id': service_id, 'TravelDate' : TravelDate}
            r = requests.post(db_addr, data = DATA)
            S = json.loads(r.text)
            for dic in S:
                if dic.get('id') not in D:
                    D[dic.get('id')] = 1
                    counter += dic.get('seats')
        except Exception as e:
            print(e)
            continue

    return counter

def new_bus_booking(id, service_id, email, From, To, TravelDate, booking_date, seats, bill):

    dbs = models.DatabaseDetails.objects.exclude(name = 'primary').filter(status = '1').order_by('size')
    counter = 0
    DATA = {'id': id, 'service_id': service_id, 'email': email, 'From': From, 'To': To, 'TravelDate': TravelDate, 'booking_date': booking_date, 'seats': seats, 'bill': bill}
    db_names = []
    for db in dbs:

        try:

            db_addr = 'http://' + db.ip_addr + ':' + db.port + BUS_BOOKING
            r = requests.post(db_addr, data = DATA)
            if r.status_code == 201:
                db_names.append(db.name)
                counter += 1
                db.size += 10
                db.save()

                if counter == replication_factor:
                    break

        except:
            continue

    if counter == replication_factor:
        new_booking = models.BookingMetaData(id = id, type = 'B', db_name_0 = db_names[0], db_name_1 = db_names[1], db_name_2 = db_names[2], start_date = TravelDate)
        new_booking.db_name = db_names[0]       # remove later
        new_booking.save()
        return 201

    return 201

def get_bus_booking_by_id(id):

    metaData = models.BookingMetaData.objects.get(id = id)
    check_primary(metaData)
    for i in range(3):

        try:

            db_name = 'db_name_' + str(i)
            db = models.DatabaseDetails.objects.get(name = getattr(metaData, db_name))
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_BOOKING_BY_ID + '/' + quote(id)
            r = requests.get(db_addr)
            return json.loads(r.text)[0]

        except:
            continue

def delete_bus_booking(id):

    try:

        metaData = models.BookingMetaData.objects.get(id = id)
        check_primary(metaData)

        primary = models.DatabaseDetails.objects.get(name = metaData.db_name_0)
        sec1 = models.DatabaseDetails.objects.get(name = metaData.db_name_1)
        sec2 = models.DatabaseDetails.objects.get(name = metaData.db_name_2)

        db_addr_0 = 'http://' + primary.ip_addr + ':' + primary.port + DELETE_BUS_BOOKING
        db_addr_1 = 'http://' + sec1.ip_addr + ':' + sec1.port + DELETE_BUS_BOOKING
        db_addr_2 = 'http://' + sec2.ip_addr + ':' + sec2.port + DELETE_BUS_BOOKING

        db_names = {'db_addr_1': sec1.name, 'db_addr_2': sec2.name}

        DATA = {'id': id}
        DATA.update({'db_addr_1': db_addr_1, 'db_addr_2': db_addr_2})

        r = requests.post(db_addr_0, data = DATA)

        if r.status_code == 200:

            primary.size -= 10
            sec1.size -= 10
            sec2.size -= 10
            primary.save()
            sec1.save()
            sec2.save()
            metaData.delete()
            UP = json.loads(r.text)
            handle_update_status(DATA, UP, 'POST', db_names)

        return r.status_code

    except Exception as e:
        print(e)
        return 400

def get_bus_booking_by_user(email):
    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    A = []
    D = {}
    for db in dbs:
        try:
            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_BOOKING_BY_USER + '/' + quote(email)
            r = requests.get(db_addr)
            S = json.loads(r.text)
            for dic in S:
                if dic.get('id') not in D:
                    A.append(dic)
                    D[dic.get('id')] = 1
        except:
            continue

    return A

def get_bus_booking_by_date(id, date):

    dbs = models.DatabaseDetails.objects.exclude(name = 'primary')
    DATA = {'id': id, 'date': date}
    D = {}
    bookings = []
    for db in dbs:

        try:

            db_addr = 'http://' + db.ip_addr + ':' + db.port + GET_BUS_BOOKING_BY_DATE
            r = requests.post(db_addr, data = DATA)
            B = json.loads(r.text)
            for booking in B:
                b_id = booking.get('id')
                if b_id not in D:
                    D[b_id] = 1
                    bookings.append(booking)

        except Exception as e:
            continue

    return bookings
