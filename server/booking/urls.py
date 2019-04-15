from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [

    path('upcoming', views.UpcomingView.as_view(), name = 'Upcoming'),
    path('past', views.PastView.as_view(), name = 'Past'),
    path('view/<slug:id>', views.BookingDetailView.as_view(), name = 'Detail'),

]
