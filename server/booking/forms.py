from django import forms
from database import utils, models
from django.utils.crypto import get_random_string

class DeleteBookingForm(forms.Form):
    password = forms.CharField(required = True, max_length = 100)
