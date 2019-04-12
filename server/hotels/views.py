from django.shortcuts import render, redirect, reverse
from urllib.parse import quote, unquote
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
from . import forms
import requests
import datetime
from django.utils import timezone
from django.utils.crypto import get_random_string

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
            available = details.get('rooms') - utils.get_hotel_bookings_by_hotel(service_id = id, in_date = request.GET.get('checkin'), out_date = request.GET.get('checkout'))
            form = forms.HotelBookForm(initial = {'available': available, 'in_date': request.GET.get('checkin'), 'out_date': request.GET.get('checkout')})
            return render(request, self.template_name, {'form': form, 'hotel': details, 'available': available, 'type': get_type(request)})

    def post(self, request, id):
        form = forms.HotelBookForm(request.POST)
        hotel = self.get_hotel_details(id)
        available = request.POST.get('available')
        if form.is_valid():
            rooms = int(form.cleaned_data.get('rooms'))
            if rooms > 0 and rooms <= int(available):
                new_id = 'H' + get_random_string(15)
                while(utils.check_booking_id(id = new_id) == False):
                    new_id = 'H' + get_random_string(15)
                db_name = utils.get_database_name()
                bill = int(hotel.get('price')) * int(form.cleaned_data.get('rooms'))
                r = utils.new_hotel_booking(db_name = db_name,
                                            id = new_id,
                                            service_id = id,
                                            email = request.session.get('email'),
                                            in_date = form.cleaned_data.get('in_date'),
                                            out_date = form.cleaned_data.get('out_date'),
                                            booking_date = datetime.date.today(),
                                            rooms = form.cleaned_data.get('rooms'),
                                            bill = bill)
                if r == 201:
                    print('BOOKING CONFIRMED')
                else:
                    return render(request, self.template_name, {'available': available, 'form': form, 'error': '1', 'msg': 'Internal Error. Try Again.', 'hotel': hotel, 'type': get_type(request)})
            else:
                return render(request, self.template_name, {'available': available, 'form': form, 'error': '1', 'msg': 'Enter Valid number of Rooms', 'hotel': hotel, 'type': get_type(request)})
        else:
            return render(request, self.template_name, {'available': available, 'form': form, 'error': '1', 'msg': 'Invalid Submission', 'hotel': hotel, 'type': get_type(request)})
