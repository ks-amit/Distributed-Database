from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [

    path('dashboard', views.DashboardView.as_view(), name = 'Dashboard'),
    path('manage', views.AdminView.as_view(), name = 'Admin'),
    path('logout', views.LogoutView.as_view(), name = 'Logout'),
    path('services', views.ServiceView.as_view(), name = 'Services'),

]
