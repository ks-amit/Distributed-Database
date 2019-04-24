from django.contrib import admin
from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [

    path('user/list', views.UserList.as_view()),
    path('user/get', views.GetUser.as_view()),
    path('user/insert', views.InsertUser.as_view()),
    path('user/update', views.UpdateUser.as_view()),
    path('bus/list', views.BusServiceList.as_view()),
    path('bus/insert', views.NewBusService.as_view()),
    path('bus/delete', views.DeleteBusService.as_view()),
    path('bus/list/email', views.BusServiceListEmail.as_view()),
    path('bus/update', views.UpdateBusService.as_view()),
    path('bus/get', views.GetBusService.as_view()),
    path('hotels/list', views.HotelServiceList.as_view()),
    path('hotels/insert', views.NewHotelService.as_view()),
    path('hotels/update', views.UpdateHotelService.as_view()),
    path('hotels/get', views.GetHotelService.as_view()),
    path('hotels/delete', views.DeleteHotelService.as_view()),
    path('hotels/list/email', views.HotelServiceListEmail.as_view()),
    path('hotels/list/city', views.GetHotelByCity.as_view()),
    path('bookings/hotel/list', views.HotelBookingList.as_view()),
    path('bookings/hotel/new', views.NewHotelBooking.as_view()),
    path('bookings/hotel/get', views.HotelBookingByHotel.as_view()),
    path('bookings/hotel/user/<str:email>', views.GetHotelBookingByUser.as_view()),
    path('bookings/hotel/id/<slug:id>', views.GetHotelBookingById.as_view()),
    path('bookings/hotel/delete', views.DeleteHotelBooking.as_view()),
    path('bookings/hotel/date', views.HotelBookingsByDate.as_view()),
    path('status', views.StatusView.as_view()),

]
