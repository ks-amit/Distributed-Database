from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [

    path('upcoming', views.UpcomingView.as_view(), name = 'Upcoming'),

]
