from django.urls import path
from . import views

app_name = 'buses'

urlpatterns = [

    path('buses', views.BusSearchView.as_view(), name = 'Search'),
    path('buses/list', views.BusDisplayView.as_view(), name = 'Display'),
    path('buses/view/<slug:id>', views.BusDetailsView.as_view(), name = 'Details'),
    path('buses/bookings/<slug:id>', views.BusBookingListView.as_view(), name = 'Bookings'),

]
