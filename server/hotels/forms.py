from django import forms
from database import utils, models
from django.utils.crypto import get_random_string

class HotelSearchForm(forms.Form):
    area = forms.CharField(max_length = 100, required = False)
    city = forms.CharField(max_length = 100, required = True)
    check_in = forms.DateField(required = True)
    check_out = forms.DateField(required = True)

class HotelBookForm(forms.Form):
    in_date = forms.CharField(max_length = 50, required = True)
    out_date = forms.CharField(max_length = 50, required = True)
    rooms = forms.IntegerField(required = True)
    available = forms.IntegerField(required = True, widget = forms.HiddenInput())

class DateForm(forms.Form):
    date = forms.DateField(required = True)
