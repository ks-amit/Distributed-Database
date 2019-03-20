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
                form = forms.NewServiceForm()
                return render(request, self.template_name, {'form': form, 'services': services, 'type': get_type(request)})
            else:
                return redirect('person:Dashboard')
        else:
            return redirect('accounts:Login')

    def post(self, request):
        if 'new_service' in request.POST:
            form = forms.NewServiceForm(request.POST)
            if form.is_valid():
                service_type = form.cleaned_data['service_type']
                id = 'B' + get_random_string(15)
                while utils.check_service_id(id) == False:
                    id = 'B' + get_random_string(15)
                db_name = utils.get_database_name()
                provider = request.session.get('email')
                r = utils.insert_bus_service(db_name, id, form.cleaned_data.get('name'), provider)
                if r == 201:
                    return redirect('person:EditBusService', id = id)
                else:
                    return render(request, self.template_name, {'form': form, 'type': get_type(request), 'error': '1', 'msg': 'Network Error'})
            else:
                return render(request, self.template_name, {'form': form, 'type': get_type(request), 'error': '1', 'msg': 'Enter Valid Details'})

class EditBusServiceView(View):
    template_name = 'person/bus_service_edit.html'

    def get_object(self, id):
        return models.ServiceMetaData.objects.filter(id = id)

    def get_user(self, email):
        user = models.UserMetaData.objects.filter(email = email)
        user = user[0]
        db_name = user.db_name
        return utils.get_user(db_name, email)

    def get_form(self, id):
        S = utils.get_bus_service_by_id(id)
        form = forms.EditServiceForm(initial = {'id': id, 'service_type': 'Bus', 'name': S.get('name'), 'bus_number': S.get('bus_number'), 'seats': S.get('seats'), 'price': S.get('price'), 'is_ready': S.get('is_ready')})
        return form

    def get(self, request, id):
        if is_authenticated(request) != None:
            service = self.get_object(id)
            if service.count() > 0:
                service = service[0]
                email = request.session.get('email')
                if email in service.provider:
                    form = self.get_form(id)
                    form1 = forms.ManagersForm()
                    form2 = forms.PasswordForm()
                    return render(request, self.template_name, {'form': form, 'form1': form1, 'form2': form2, 'service': service, 'type': get_type(request)})
                else:
                    print('NOT FOUND')
            else:
                print('NOT FOUND')
        else:
            return redirect('person:Dashboard')

    def post(self, request, id):
        service = self.get_object(id)
        service = service[0]
        if 'delete_service' in request.POST:
            user = self.get_user(request.session.get('email'))
            if check_password(request.POST.get('password'), user.get('password')):
                r = utils.delete_bus_service(id = id)
                if r == 200:
                    return redirect('person:Services')
                else:
                    return render(request, self.template_name, {'form': self.get_form(id), 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'error2': '1', 'msg2': 'Network Error', 'service': service, 'type': get_type(request)})
            else:
                return render(request, self.template_name, {'form': self.get_form(id), 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'error2': '1', 'msg2': 'Incorrect Password', 'service': service, 'type': get_type(request)})
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
                        return render(request, self.template_name, {'form': self.get_form(id), 'form1': form1, 'form2': forms.PasswordForm(), 'error1': '1', 'msg1': 'Network Error', 'service': service, 'type': get_type(request)})
                return redirect('person:EditBusService', id = id)
            else:
                return render(request, self.template_name, {'form': self.get_form(id), 'form1': form1, 'form2': forms.PasswordForm(), 'error1': '1', 'service': service, 'type': get_type(request)})
        elif 'edit_service' in request.POST:
            form = forms.EditServiceForm(request.POST)
            if form.is_valid():
                is_ready = None
                if form.cleaned_data.get('is_ready') == 'on':
                    is_ready = True
                r = utils.update_bus_service(   name = form.cleaned_data.get('name'),
                                                price = form.cleaned_data.get('price'),
                                                bus_number = form.cleaned_data.get('bus_number'),
                                                seats = form.cleaned_data.get('seats'),
                                                is_ready = is_ready,
                                                id = id)
                if r == 200:
                    return render(request, self.template_name, {'form': self.get_form(id), 'success': '1', 'msg': 'INFORMATION UPDATED', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'service': service, 'type': get_type(request)})
                else:
                    return render(request, self.template_name, {'form': self.get_form(id), 'error': '1', 'msg': 'NETWORK ERROR', 'form1': forms.ManagersForm(), 'form2': forms.PasswordForm(), 'service': service, 'type': get_type(request)})
            else:
                print('NOT VALID')

class DeleteManagerView(View):
    template_name = 'person/bus_service_edit.html'

    def get_object(self, id):
        return models.ServiceMetaData.objects.filter(id = id)

    def get(self, request, id, email):
        service = self.get_object(id)
        if not service:
            print('NOT FOUND')
        else:
            service = service[0]
            if len(service.provider) == 1:
                return redirect('person:EditBusService', id = id)
            else:
                E = service.provider[int(email)]
                r = utils.update_bus_service(id = id, provider = E, provider_code = 'REMOVE')
                if r == 200:
                    service.provider.remove(E)
                    service.save()
                return redirect('person:EditBusService', id = id)

class LogoutView(View):

    def get(self, request):
        request.session.update({'email': None, 'type': None})
        return redirect('accounts:Login')
