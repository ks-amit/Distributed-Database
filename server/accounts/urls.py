from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [

    path('login', views.LoginView.as_view(), name = 'Login'),
    path('register', views.SignupView.as_view(), name = 'Signup'),
    path('forgot', views.ForgotView.as_view(), name = 'Forgot'),
    path('reset', views.PasswordResetView.as_view(), name = 'Reset'),

]
