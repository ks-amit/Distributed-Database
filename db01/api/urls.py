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

]
