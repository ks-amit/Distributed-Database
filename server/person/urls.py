from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [

    path('dashboard', views.DashboardView.as_view(), name = 'Dashboard'),
    path('manage', views.AdminView.as_view(), name = 'Admin'),
    path('logout', views.LogoutView.as_view(), name = 'Logout'),
    path('services', views.ServiceView.as_view(), name = 'Services'),
    path('service/<slug:id>', views.EditServiceView.as_view(), name = 'EditService'),
    path('delete_manager_from_service/<slug:id>/<slug:email>', views.DeleteManagerView.as_view(), name = 'DeleteManager'),
    path('delete_bus_route/<slug:id>/<int:index>', views.DeleteRouteView.as_view(), name = 'DeleteBusRoute'),

]
