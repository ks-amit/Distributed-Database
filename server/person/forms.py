from django import forms
from database import utils, models
from django.utils.crypto import get_random_string

class UserPrivilageForm(forms.Form):
    CHOICES = ( ('U', 'Standard User'),
                ('A', 'Admin'),
                ('S', 'Service Provider'),)
    email = forms.EmailField(max_length = 100, required = True)
    privilage = forms.ChoiceField(choices = CHOICES, widget = forms.Select)

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def clean_privilage(self):
        privilage = self.cleaned_data['privilage']
        email = self.cleaned_data['email']
        user = self.get_object(email)
        if user.count() > 0:
            user = user[0]
            r = utils.update_user(user.db_name, user.email, type = privilage)
            if r == 200:
                return privilage
            else:
                raise forms.ValidationError('Network Error')
        else:
            raise forms.ValidationError('User not found')

class PasswordForm(forms.Form):
    password = forms.CharField(required = True, max_length = 100)

class ManagersForm(forms.Form):
    email = forms.EmailField(max_length = 100, required = True)

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.get_object(email)
        if user.count() > 0:
            user = user[0]
            user = utils.get_user(user.db_name, user.email)
            if user.get('type') == 'S':
                return email
            else:
                raise forms.ValidationError('User not a service provider')
        else:
            raise forms.ValidationError('User does not exist')


class NewServiceForm(forms.Form):
    CHOICES = ( ('B', 'Bus Service'),
                ('H', 'Hotel Service'),)
    name = forms.CharField(max_length = 100, required = True)
    service_type = forms.ChoiceField(choices = CHOICES, widget = forms.Select)

class EditBusServiceForm(forms.Form):
    CHOICES = ( ('B', 'Bus Service'),
                ('H', 'Hotel Service'),)
    id = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs={'readonly': True}))
    name = forms.CharField(max_length = 100, required = True)
    service_type = forms.CharField(widget = forms.TextInput(attrs={'readonly': True}))
    bus_number = forms.CharField(max_length = 20, required = True)
    seats = forms.IntegerField(required = True)
    price = forms.IntegerField(required = True)
    is_ready = forms.BooleanField(required = False)

class EditRouteForm(forms.Form):
    stop_name = forms.CharField(max_length = 100, required = True)
    day = forms.IntegerField(min_value = 0, required = True)
    time_hour = forms.IntegerField(min_value = 0, max_value = 23, required = True)
    time_mins = forms.IntegerField(min_value = 0, max_value = 59, required = True)
    boarding_point = forms.CharField(max_length = 100, required = True)

class EditHotelServiceForm(forms.Form):
    CHOICES = ( ('B', 'Bus Service'),
                ('H', 'Hotel Service'),)
    id = forms.CharField(max_length = 100, required = True, widget = forms.TextInput(attrs={'readonly': True}))
    name = forms.CharField(max_length = 100, required = True)
    service_type = forms.CharField(widget = forms.TextInput(attrs={'readonly': True}))
    city = forms.CharField(max_length = 100, required = True)
    area = forms.CharField(max_length = 100, required = True)
    address = forms.CharField(max_length = 200, required = True)
    description = forms.CharField(required = True, widget = forms.Textarea)
    rooms = forms.IntegerField(required = True)
    price = forms.IntegerField(required = True)
    is_ready = forms.BooleanField(required = False)
    check_in = forms.TimeField(required = True)
    check_out = forms.TimeField(required = True)
