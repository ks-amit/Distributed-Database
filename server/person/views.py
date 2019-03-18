from django.shortcuts import render, redirect
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
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

    def get(self, request):
        if is_authenticated(request) != None:
            if get_type(request) == 'S':
                form = forms.NewServiceForm()
                return render(request, self.template_name, {'form': form, 'type': get_type(request)})
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
                    print('UPDATED')
                    return 0
                else:
                    return render(request, self.template_name, {'form': form, 'type': get_type(request), 'error': '1', 'msg': 'Network Error'})
            else:
                return render(request, self.template_name, {'form': form, 'type': get_type(request), 'error': '1', 'msg': 'Enter Valid Details'})

class LogoutView(View):

    def get(self, request):
        request.session.update({'email': None, 'type': None})
        return redirect('accounts:Login')
