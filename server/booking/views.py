from django.shortcuts import render, redirect, reverse
from urllib.parse import quote, unquote
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
from django.contrib.auth.hashers import make_password, check_password
from . import forms
import datetime

class UpcomingView(View):

    template_name = 'booking/upcoming_hotels.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            if request.GET.get('type') != 'buses':
                hotel_bookings = utils.get_hotel_booking_by_user(request.session.get('email'))
                upcoming_bookings = []
                for booking in hotel_bookings:
                    date = datetime.datetime.strptime(booking.get('out_date'), "%Y-%m-%d").date()
                    if date < datetime.date.today():
                        continue
                    else:
                        hotel_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        booking.update({'service_name': hotel_detail.name})
                        upcoming_bookings.append(booking)
                return render(request, self.template_name, {'hotel_bookings': upcoming_bookings, 'type': get_type(request)})
            else:
                print('BUS BOOKINGS')

class PastView(View):

    template_name = 'booking/past_hotels.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            if request.GET.get('type') != 'buses':
                hotel_bookings = utils.get_hotel_booking_by_user(request.session.get('email'))
                past_bookings = []
                for booking in hotel_bookings:
                    date = datetime.datetime.strptime(booking.get('out_date'), "%Y-%m-%d").date()
                    if date >= datetime.date.today():
                        continue
                    else:
                        hotel_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        booking.update({'service_name': hotel_detail.name})
                        past_bookings.append(booking)
                return render(request, self.template_name, {'hotel_bookings': past_bookings, 'type': get_type(request)})
            else:
                print('BUS BOOKINGS')


class BookingDetailView(View):

    template_name = 'booking/details.html'

    def get(self, request, id):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            form = forms.DeleteBookingForm()
            if id[0] == 'H':
                booking_details = models.BookingMetaData.objects.filter(id=id)
                if not booking_details:
                    print('NOT FOUND')
                else:
                    booking = utils.get_hotel_booking_by_id(id)
                    if booking.get('email') != request.session.get('email'):
                        print('NOT FOUND')
                    else:
                        hotel = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        return render(request, self.template_name, {'form': form, 'booking': booking, 'hotel': hotel, 'type': get_type(request)})

    def post(self, request, id):
        userInfo = models.UserMetaData.objects.get(email = request.session.get('email'))
        db_name = userInfo.db_name
        if id[0] == 'H':
            booking = utils.get_hotel_booking_by_id(id)
            hotel = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
            form = forms.DeleteBookingForm(request.POST)
            if form.is_valid():
                user = utils.get_user(db_name, request.session.get('email'))
                if check_password(form.cleaned_data.get('password'), user.get('password')) == True:
                    r = utils.delete_hotel_booking(id)
                    if r == 200:
                        return redirect('person:Dashboard')
                    else:
                        return render(request, self.template_name, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Network Error', 'booking': booking, 'hotel': hotel, 'type': get_type(request)})
                else:
                    return render(request, self.template_name, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Incorrect Password', 'booking': booking, 'hotel': hotel, 'type': get_type(request)})
            else:
                return render(request, self.template_name, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Fields cannot be empty', 'booking': booking, 'hotel': hotel, 'type': get_type(request)})
