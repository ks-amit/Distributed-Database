from django.shortcuts import render, redirect
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
from django.contrib.auth.hashers import make_password, check_password
from . import forms
from django.utils.crypto import get_random_string

class DashboardView(View):
    template_name = 'person/dashboard.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            return render(request, self.template_name, {'type': get_type(request)})

class AdminView(View):
    template_name = 'person/admin.html'

    def get(self, request):
        if is_authenticated(request) != None and get_type(request) == 'A':
            form1 = forms.UserPrivilageForm()
            form2 = forms.NewServiceForm()
            return render(request, self.template_name, {'form1': form1, 'form2': form2, 'type': get_type(request)})
        else:
            return redirect('accounts:Login')

    def post(self, request):
        form1 = forms.UserPrivilageForm()
        form2 = forms.NewServiceForm()
        if 'user_privilage' in request.POST:
            form1 = forms.UserPrivilageForm(request.POST)
            if form1.is_valid():
                return render(request, self.template_name, {'form1': forms.UserPrivilageForm(), 'form2': forms.NewServiceForm(), 'type': get_type(request), 'success1': '1', 'msg1': 'Request Processed'})
            else:
                return render(request, self.template_name, {'form1': form1, 'form2': forms.NewServiceForm(), 'type': get_type(request), 'error1': '1'})
        elif 'new_service' in request.POST:
            form2 = forms.NewServiceForm(request.POST)
            print(request.POST)

class ServiceView(View):
    template_name = 'person/services.html'

    def get_object(self, email):
        return models.ServiceMetaData.objects.filter(provider__contains=list([email]))

    def get(self, request):
        if is_authenticated(request) != None:
            if get_type(request) == 'S':
                services = utils.get_bus_service_by_email(request.session.get('email'))
                services1 = utils.get_hotel_service_by_email(request.session.get('email'))
                form = forms.NewServiceForm()
                return render(request, self.template_name, {'form': form, 'services': services, 'services1': services1, 'type': get_type(request)})
            else:
                return redirect('person:Dashboard')
        else:
            return redirect('accounts:Login')

    def post(self, request):
        services = utils.get_bus_service_by_email(request.session.get('email'))
        services1 = utils.get_hotel_service_by_email(request.session.get('email'))
        if 'new_service' in request.POST and request.POST.get('service_type') == 'B':
            form = forms.NewServiceForm(request.POST)
            if form.is_valid():
                service_type = form.cleaned_data.get('service_type')
                id = 'B' + get_random_string(15)
                while utils.check_service_id(id) == False:
                    id = 'B' + get_random_string(15)
                db_name = utils.get_database_name()
                provider = request.session.get('email')
                r = utils.insert_bus_service(db_name, id, form.cleaned_data.get('name'), provider)
                if r == 201:
                    return redirect('person:EditService', id = id)
                else:
                    return render(request, self.template_name, {'form': form, 'services': services, 'services1': services1, 'type': get_type(request), 'error': '1', 'msg': 'Network Error'})
            else:
                return render(request, self.template_name, {'form': form, 'services': services, 'services1': services1, 'type': get_type(request), 'error': '1', 'msg': 'Invalid Details'})
        elif 'new_service' in request.POST and request.POST.get('service_type') == 'H':
            form = forms.NewServiceForm(request.POST)
            if form.is_valid():
                service_type = form.cleaned_data.get('service_type')
                id = 'H' + get_random_string(15)
                while utils.check_service_id(id) == False:
                    id = 'H' + get_random_string(15)
                db_name = utils.get_database_name()
                provider = request.session.get('email')
                r = utils.insert_hotel_service(db_name, id, form.cleaned_data.get('name'), provider)
                if r == 201:
                    return redirect('person:EditService', id = id)
                else:
                    return render(request, self.template_name, {'form': form, 'services': services, 'services1': services1, 'type': get_type(request), 'error': '1', 'msg': 'Network Error'})
            else:
                return render(request, self.template_name, {'form': form, 'services': services, 'services1': services1, 'type': get_type(request), 'error': '1', 'msg': 'Invalid Details'})


class EditServiceView(View):
    template_name = 'person/bus_service_edit.html'
    template_name_1 = 'person/hotel_service_edit.html'

    def get_object(self, id):
        return models.ServiceMetaData.objects.filter(id = id)

    def get_user(self, email):
        user = models.UserMetaData.objects.filter(email = email)
        user = user[0]
        db_name = user.db_name
        return utils.get_user(db_name, email)

    def get_form(self, id):
        S = utils.get_bus_service_by_id(id)
        form = forms.EditBusServiceForm(initial = {'id': id, 'service_type': 'Bus', 'name': S.get('name'), 'bus_number': S.get('bus_number'), 'seats': S.get('seats'), 'price': S.get('price'), 'is_ready': S.get('is_ready')})
        return form

    def get_form_1(self, id):
        S = utils.get_hotel_service_by_id(id)
        form = forms.EditHotelServiceForm(initial = {'id': id, 'service_type': 'Hotel', 'name': S.get('name'), 'description': S.get('description'), 'city': S.get('city'), 'address': S.get('address'), 'area': S.get('area'), 'rooms': S.get('rooms'), 'check_in': S.get('check_in'), 'check_out': S.get('check_out'), 'price': S.get('price'), 'is_ready': S.get('is_ready')})
        return form

    def get_service(self, id):
        S = utils.get_bus_service_by_id(id)
        S.update({'combined_list': zip(S.get('route'), S.get('timing'), S.get('boarding_point'))})
        print(S)
        return S

    def get_service_1(self, id):
        S = utils.get_hotel_service_by_id(id)
        return S

    def get(self, request, id):
        if is_authenticated(request) != None:
            service = self.get_object(id)
            if service.count() > 0:
                service = service[0]
                if service.type == 'B':
                    email = request.session.get('email')
                    if email in service.provider:
                        form = self.get_form(id)
                        form1 = forms.ManagersForm()
                        form2 = forms.PasswordForm()
                        form3 = forms.EditRouteForm()
                        return render(request, self.template_name, {'form': form, 'form1': form1, 'form2': form2, 'form3': form3, 'service': self.get_service(id), 'type': get_type(request)})
                    else:
                        print('NOT FOUND')

                elif service.type == 'H':
                    email = request.session.get('email')
                    if email in service.provider:
                        form1 = forms.ManagersForm()
                        form2 = forms.PasswordForm()
                        return render(request, self.template_name_1, {'form': self.get_form_1(id), 'form1': form1, 'form2': form2, 'service': self.get_service_1(id), 'type': get_type(request)})

            else:
                print('NOT FOUND')
        else:
            return redirect('person:Dashboard')

    def post(self, request, id):
        service = self.get_object(id)
        service = service[0]
        if service.type == 'B':
            if 'delete_service' in request.POST:
                user = self.get_user(request.session.get('email'))
                if check_password(request.POST.get('password'), user.get('password')):
                    r = utils.delete_bus_service(id = id)
                    if r == 200:
                        return redirect('person:Services')
                    else:
                        return render(request, self.template_name, {'form': self.get_form(id), 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'error2': '1', 'msg2': 'Network Error', 'service': self.get_service(id), 'type': get_type(request)})
                else:
                    return render(request, self.template_name, {'form': self.get_form(id), 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'error2': '1', 'msg2': 'Incorrect Password', 'service': self.get_service(id), 'type': get_type(request)})
            elif 'add_manager' in request.POST:
                form1 = forms.ManagersForm(request.POST)
                if form1.is_valid():
                    email = form1.cleaned_data.get('email')
                    if email not in service.provider:
                        r = utils.update_bus_service(id = id, provider = email, provider_code = 'ADD')
                        if r == 200:
                            service.provider.append(email)
                            service.save()
                        else:
                            return render(request, self.template_name, {'form': self.get_form(id), 'form1': form1, 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'error1': '1', 'msg1': 'Network Error', 'service': self.get_service(id), 'type': get_type(request)})
                    return redirect('person:EditService', id = id)
                else:
                    return render(request, self.template_name, {'form': self.get_form(id), 'form1': form1, 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'error1': '1', 'service': self.get_service(id), 'type': get_type(request)})
            elif 'edit_service' in request.POST:
                form = forms.EditBusServiceForm(request.POST)
                if form.is_valid():
                    r = utils.update_bus_service(   name = form.cleaned_data.get('name'),
                                                    price = form.cleaned_data.get('price'),
                                                    bus_number = form.cleaned_data.get('bus_number'),
                                                    seats = form.cleaned_data.get('seats'),
                                                    is_ready = form.cleaned_data.get('is_ready'),
                                                    id = id)
                    if r == 200:
                        service.name = form.cleaned_data.get('name')
                        service.capacity = int(form.cleaned_data.get('seats'))
                        service.save()
                        return render(request, self.template_name, {'form': self.get_form(id), 'success': '1', 'msg': 'INFORMATION UPDATED', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'service': self.get_service(id), 'type': get_type(request)})
                    else:
                        return render(request, self.template_name, {'form': self.get_form(id), 'error': '1', 'msg': 'NETWORK ERROR', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'service': self.get_service(id), 'type': get_type(request)})
                else:
                    return render(request, self.template_name, {'form': self.get_form(id), 'error': '1', 'msg': 'INVALID DETAILS', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'service': self.get_service(id), 'type': get_type(request)})
            elif 'edit_route' in request.POST:
                form3 = forms.EditRouteForm(request.POST)
                if form3.is_valid():
                    time = str(form3.cleaned_data.get('day')) + ':' + str(form3.cleaned_data.get('time_hour')) + ':' + str(form3.cleaned_data.get('time_mins'))
                    r = utils.update_bus_service(id = id, boarding_point = form3.cleaned_data.get('boarding_point'), route = form3.cleaned_data.get('stop_name'), route_code = 'ADD', timing = time, timing_code = 'ADD', boarding_code = 'ADD')
                    if r == 200:
                        return render(request, self.template_name, {'form': self.get_form(id), 'success3': '1', 'msg3': 'Bus Route Updated', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': forms.EditRouteForm(), 'service': self.get_service(id), 'type': get_type(request)})
                    else:
                        return render(request, self.template_name, {'form': self.get_form(id), 'error3': '1', 'msg3': 'Network Error', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': form3, 'service': self.get_service(id), 'type': get_type(request)})
                else:
                    return render(request, self.template_name, {'form': self.get_form(id), 'error3': '1', 'msg3': 'INVALID DETAILS', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'form3': form3, 'service': self.get_service(id), 'type': get_type(request)})

        elif service.type == 'H':
            if 'add_manager' in request.POST:
                form1 = forms.ManagersForm(request.POST)
                if form1.is_valid():
                    email = form1.cleaned_data.get('email')
                    if email not in service.provider:
                        r = utils.update_hotel_service(id = id, provider = email, provider_code = 'ADD')
                        if r == 200:
                            service.provider.append(email)
                            service.save()
                            return redirect('person:EditService', id = id)
                        else:
                            return render(request, self.template_name_1, {'form': self.get_form_1(id), 'form1': form1, 'form2': forms.PasswordForm(), 'error1': '1', 'msg1': 'Network Error', 'service': self.get_service_1(id), 'type': get_type(request)})
                    else:
                        return redirect('person:EditService', id = id)
                else:
                    return render(request, self.template_name_1, {'form': self.get_form_1(id), 'form1': form1, 'form2': forms.PasswordForm(), 'error1': '1', 'service': self.get_service_1(id), 'type': get_type(request)})

            elif 'delete_service' in request.POST:
                user = self.get_user(request.session.get('email'))
                if check_password(request.POST.get('password'), user.get('password')):
                    r = utils.delete_hotel_service(id = id)
                    if r == 200:
                        return redirect('person:Services')
                    else:
                        return render(request, self.template_name_1, {'form': self.get_form_1(id), 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'error2': '1', 'msg2': 'Network Error', 'service': self.get_service_1(id), 'type': get_type(request)})
                else:
                    return render(request, self.template_name_1, {'form': self.get_form_1(id), 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'error2': '1', 'msg2': 'Incorrect Password', 'service': self.get_service_1(id), 'type': get_type(request)})

            elif 'edit_service' in request.POST:
                form = forms.EditHotelServiceForm(request.POST)
                if form.is_valid():
                    r = utils.update_hotel_service( name = form.cleaned_data.get('name'),
                                                    price = form.cleaned_data.get('price'),
                                                    city = form.cleaned_data.get('city'),
                                                    area = form.cleaned_data.get('area'),
                                                    rooms = form.cleaned_data.get('rooms'),
                                                    address = form.cleaned_data.get('address'),
                                                    is_ready = form.cleaned_data.get('is_ready'),
                                                    id = id,
                                                    description = form.cleaned_data.get('description'),
                                                    check_in = form.cleaned_data.get('check_in'),
                                                    check_out = form.cleaned_data.get('check_out'))
                    if r == 200:
                        service.name = form.cleaned_data.get('name')
                        service.capacity = int(form.cleaned_data.get('rooms'))
                        service.save()
                        return render(request, self.template_name_1, {'form': self.get_form_1(id), 'success': '1', 'msg': 'INFORMATION UPDATED', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'service': self.get_service_1(id), 'type': get_type(request)})
                    else:
                        return render(request, self.template_name_1, {'form': self.get_form_1(id), 'error': '1', 'msg': 'NETWORK ERROR', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'service': self.get_service_1(id), 'type': get_type(request)})
                else:
                    print(form.errors)
                    return render(request, self.template_name_1, {'form': self.get_form_1(id), 'error': '1', 'msg': 'INVALID DETAILS', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'service': self.get_service_1(id), 'type': get_type(request)})

class DeleteManagerView(View):

    def get_object(self, id):
        return models.ServiceMetaData.objects.filter(id = id)

    def get(self, request, id, email):
        service = self.get_object(id)
        if not service:
            print('NOT FOUND')
        else:
            service = service[0]
            if len(service.provider) == 1:
                return redirect('person:EditService', id = id)
            else:
                E = service.provider[int(email)]
                if service.type == 'B':
                    r = utils.update_bus_service(id = id, provider = E, provider_code = 'REMOVE')
                    if r == 200:
                        service.provider.remove(E)
                        service.save()
                elif service.type == 'H':
                    r = utils.update_hotel_service(id = id, provider = E, provider_code = 'REMOVE')
                    if r == 200:
                        service.provider.remove(E)
                        service.save()
                return redirect('person:EditService', id = id)

class DeleteRouteView(View):

    def get_object(self, id):
        return models.ServiceMetaData.objects.filter(id = id)

    def get(self, request, id, index):
        service = self.get_object(id)
        if not service:
            print('NOT FOUND')
        else:
            r = utils.update_bus_service(id = id, route = index, timing = index, boarding_point = index, route_code = 'REMOVE', timing_code = 'REMOVE', boarding_code = 'REMOVE')
            if r == 200:
                return redirect('person:EditService', id = id)
            else:
                return redirect('person:EditService', id = id)

class LogoutView(View):

    def get(self, request):
        request.session.update({'email': None, 'type': None})
        return redirect('accounts:Login')
