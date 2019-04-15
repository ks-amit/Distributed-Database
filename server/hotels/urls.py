from django.urls import path
from . import views

app_name = 'hotels'

urlpatterns = [

    path('hotels', views.HotelSearchView.as_view(), name = 'Search'),
    path('hotels/list', views.HotelDisplayView.as_view(), name = 'Display'),
    path('hotels/view/<slug:id>', views.HotelDetailsView.as_view(), name = 'Details'),
    path('hotels/bookings/<slug:id>', views.HotelBookingListView.as_view(), name = 'Bookings'),

]
