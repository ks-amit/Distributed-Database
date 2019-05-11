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
    template_name_1 = 'booking/upcoming_buses.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            if request.GET.get('type') != 'buses':
                hotel_bookings = utils.get_hotel_booking_by_user(request.session.get('email'))
                upcoming_bookings = []
                for booking in hotel_bookings:
                    date = datetime.datetime.strptime(booking.get('in_date'), "%Y-%m-%d").date()
                    if date < datetime.date.today():
                        continue
                    else:
                        hotel_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        booking.update({'service_name': hotel_detail.name})
                        upcoming_bookings.append(booking)
                return render(request, self.template_name, {'hotel_bookings': upcoming_bookings, 'type': get_type(request)})
            else:
                bus_bookings = utils.get_bus_booking_by_user(request.session.get('email'))
                upcoming_bookings = []
                for booking in bus_bookings:
                    date = datetime.datetime.strptime(booking.get('TravelDate'), "%Y-%m-%d").date()
                    if date < datetime.date.today():
                        continue
                    else:
                        bus_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        booking.update({'service_name': bus_detail.name})
                        upcoming_bookings.append(booking)
                return render(request, self.template_name_1, {'bus_bookings': upcoming_bookings, 'type': get_type(request)})

class PastView(View):

    template_name = 'booking/past_hotels.html'
    template_name_1 = 'booking/past_buses.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            if request.GET.get('type') != 'buses':
                hotel_bookings = utils.get_hotel_booking_by_user(request.session.get('email'))
                past_bookings = []
                for booking in hotel_bookings:
                    date = datetime.datetime.strptime(booking.get('in_date'), "%Y-%m-%d").date()
                    if date >= datetime.date.today():
                        continue
                    else:
                        hotel_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        booking.update({'service_name': hotel_detail.name})
                        past_bookings.append(booking)
                return render(request, self.template_name, {'hotel_bookings': past_bookings, 'type': get_type(request)})
            else:
                bus_bookings = utils.get_bus_booking_by_user(request.session.get('email'))
                upcoming_bookings = []
                for booking in bus_bookings:
                    date = datetime.datetime.strptime(booking.get('TravelDate'), "%Y-%m-%d").date()
                    if date >= datetime.date.today():
                        continue
                    else:
                        bus_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                        booking.update({'service_name': bus_detail.name})
                        upcoming_bookings.append(booking)
                return render(request, self.template_name_1, {'bus_bookings': upcoming_bookings, 'type': get_type(request)})



class BookingDetailView(View):

    template_name = 'booking/details.html'
    template_name_1 = 'booking/details_bus.html'

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
                    try:
                        booking = utils.get_hotel_booking_by_id_rep(id)
                        in_date = datetime.datetime.strptime(booking.get('in_date'), "%Y-%m-%d").date()
                        cancel_option = datetime.date.today() < in_date
                        if booking.get('email') != request.session.get('email'):
                            print('NOT FOUND')
                        else:
                            hotel = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                            return render(request, self.template_name, {'form': form, 'booking': booking, 'hotel': hotel, 'cancel_option': cancel_option, 'type': get_type(request)})
                    except:
                        print('INTERNAL ERROR')
            else:
                booking_details = models.BookingMetaData.objects.filter(id=id)
                if not booking_details:
                    print('NOT FOUND')
                else:
                    try:
                        booking = utils.get_bus_booking_by_id(id)
                        TravelDate = datetime.datetime.strptime(booking.get('TravelDate'), "%Y-%m-%d").date()
                        cancel_option = datetime.date.today() < TravelDate
                        if booking.get('email') != request.session.get('email'):
                            print('NOT FOUND')
                        else:
                            bus = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                            return render(request, self.template_name_1, {'form': form, 'booking': booking, 'bus': bus, 'cancel_option': cancel_option, 'type': get_type(request)})
                    except:
                        print('INTERNAL ERROR')

    def post(self, request, id):
        userInfo = models.UserMetaData.objects.get(email = request.session.get('email'))
        if id[0] == 'H':
            booking = utils.get_hotel_booking_by_id_rep(id)
            in_date = datetime.datetime.strptime(booking.get('in_date'), "%Y-%m-%d").date()
            cancel_option = datetime.date.today() < in_date
            if cancel_option == False:
                return redirect('booking:Detail', id = id)
            else:
                hotel = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                form = forms.DeleteBookingForm(request.POST)
                if form.is_valid():
                    user = utils.get_user_rep(userInfo)
                    if check_password(form.cleaned_data.get('password'), user.get('password')) == True:
                        r = utils.delete_hotel_booking_rep(id)
                        if r == 200:
                            return redirect('person:Dashboard')
                        else:
                            return render(request, self.template_name, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Network Error', 'booking': booking, 'cancel_option': cancel_option, 'hotel': hotel, 'type': get_type(request)})
                    else:
                        return render(request, self.template_name, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Incorrect Password', 'booking': booking, 'cancel_option': cancel_option, 'hotel': hotel, 'type': get_type(request)})
                else:
                    return render(request, self.template_name, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Fields cannot be empty', 'cancel_option': cancel_option, 'booking': booking, 'hotel': hotel, 'type': get_type(request)})

        else:
            booking = utils.get_bus_booking_by_id(id)
            TravelDate = datetime.datetime.strptime(booking.get('TravelDate'), "%Y-%m-%d").date()
            cancel_option = datetime.date.today() < TravelDate
            if cancel_option == False:
                return redirect('booking:Detail', id = id)
            else:
                bus = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                form = forms.DeleteBookingForm(request.POST)
                if form.is_valid():
                    user = utils.get_user_rep(userInfo)
                    if check_password(form.cleaned_data.get('password'), user.get('password')) == True:
                        r = utils.delete_bus_booking(id)
                        if r == 200:
                            return redirect('person:Dashboard')
                        else:
                            return render(request, self.template_name_1, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Internal Error! Try again after some time.', 'booking': booking, 'cancel_option': cancel_option, 'bus': bus, 'type': get_type(request)})
                    else:
                        return render(request, self.template_name_1, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Incorrect Password', 'booking': booking, 'cancel_option': cancel_option, 'bus': bus, 'type': get_type(request)})
                else:
                    return render(request, self.template_name_1, {'form': forms.DeleteBookingForm(), 'error': '1', 'msg': 'Fields cannot be empty', 'cancel_option': cancel_option, 'booking': booking, 'bus': bus, 'type': get_type(request)})
