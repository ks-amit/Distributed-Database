from django.shortcuts import render, redirect, reverse
from urllib.parse import quote, unquote
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
from . import forms
import requests
import datetime

class HotelSearchView(View):
    template_name = 'hotels/search.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            form = forms.HotelSearchForm()
            return render(request, self.template_name, {'form': form, 'type': get_type(request)})

    def post(self, request):
        form = forms.HotelSearchForm(request.POST)
        if form.is_valid():
            date1 = form.cleaned_data.get('check_in')
            date2 = form.cleaned_data.get('check_out')
            today = datetime.date.today()
            if(date1 < date2 and date1 >= today):
                if form.cleaned_data.get('area') == None or form.cleaned_data.get('area') == '':
                    query_string = 'city=' + quote(str(form.cleaned_data.get('city'))) + '&checkin=' + quote(str(date1)) + '&checkout=' + quote(str(date2))
                else:
                    query_string = 'city=' + quote(str(form.cleaned_data.get('city'))) + '&area=' + quote(str(form.cleaned_data.get('area'))) + '&checkin=' + quote(str(date1)) + '&checkout=' + quote(str(date2))
                return redirect(reverse('hotels:Display') + '?' + query_string)
            else:
                return render(request, self.template_name, {'form': form, 'error': '1', 'msg': 'Incorrect Dates', 'type': get_type(request)})
        else:
            return render(request, self.template_name, {'form': form, 'error': '1', 'msg': 'Fill in valid details only', 'type': get_type(request)})

class HotelDisplayView(View):
    template_name = 'hotels/display.html'

    def get_hotels(self, city, area = None):
        return utils.get_hotel_services_city(city, area)

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            hotels = self.get_hotels(request.GET.get('city'), request.GET.get('area'))
            return render(request, self.template_name, {'hotels': hotels, 'type': get_type(request)})

class HotelDetailsView(View):
    template_name = 'hotels/details.html'

    def get_hotel_details(self, id):
        return utils.get_hotel_service_by_id(id)

    def get(self, request, id):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            details = self.get_hotel_details(id)
            return render(request, self.template_name, {'hotel': details, 'type': get_type(request)})
