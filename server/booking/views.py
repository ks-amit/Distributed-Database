from django.shortcuts import render, redirect, reverse
from urllib.parse import quote, unquote
from django.views import View
from database import utils, models
from accounts.authentication import is_authenticated, get_type
from . import forms

class UpcomingView(View):

    template_name = 'booking/upcoming.html'

    def get(self, request):
        if is_authenticated(request) == None:
            return redirect('accounts:Login')
        else:
            hotel_bookings = utils.get_hotel_booking_by_user(request.session.get('email'))
            for booking in hotel_bookings:
                hotel_detail = models.ServiceMetaData.objects.get(id = booking.get('service_id'))
                booking.update({'service_name': hotel_detail.name})
            return render(request, self.template_name, {'hotel_bookings': hotel_bookings, 'type': get_type(request)})
