from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [

    path('dashboard', views.DashboardView.as_view(), name = 'Dashboard'),
    path('manage', views.AdminView.as_view(), name = 'Admin'),
    path('logout', views.LogoutView.as_view(), name = 'Logout'),
    path('services', views.ServiceView.as_view(), name = 'Services'),
    path('service/<slug:id>', views.EditBusServiceView.as_view(), name = 'EditBusService'),
    path('delete_manager_from_service/<slug:id>/<slug:email>', views.DeleteManagerView.as_view(), name = 'DeleteManager'),

]
