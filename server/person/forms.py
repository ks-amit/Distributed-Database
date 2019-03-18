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


class NewServiceForm(forms.Form):
    CHOICES = ( ('B', 'Bus Service'),
                ('H', 'Hotel Service'),)
    name = forms.CharField(max_length = 100, required = True)
    service_type = forms.ChoiceField(choices = CHOICES, widget = forms.Select)
