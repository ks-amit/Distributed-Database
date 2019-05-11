from django import forms
from database import utils, models
from django.utils.crypto import get_random_string

class BusSearchForm(forms.Form):
    From = forms.CharField(max_length = 100, required = True)
    To = forms.CharField(max_length = 100, required = True)
    TravelDate = forms.DateField(required = True)

class BusBookForm(forms.Form):
    From = forms.CharField(max_length = 50, required = True)
    To = forms.CharField(max_length = 50, required = True)
    TravelDate = forms.CharField(max_length = 50, required = True)
    seats = forms.IntegerField(required = True)
    available = forms.IntegerField(required = True, widget = forms.HiddenInput())

class DateForm(forms.Form):
    date = forms.DateField(required = True)
