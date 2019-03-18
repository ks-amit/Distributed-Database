from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from database import models
from . import forms
from database import utils
from . import mail

class LoginView(View):
    template_name = 'accounts/login.html'

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def get(self, request):
        return render(request, self.template_name, {'form': forms.LoginForm()})

    def post(self, request):
        try:
            user = self.get_object(request.POST['email'])
            if user.count() == 0:
                return render(request, self.template_name, {'form': forms.LoginForm(), 'error': '1', 'msg': 'User does not exist. SignUp to proceed'})
            else:
                user = user[0]
                r = utils.get_user(user.db_name, user.email)
                pass2 = r.get('password')
                if check_password(request.POST['password'], pass2) == True:
                    request.session.update({'email': user.email, 'type': r.get('type')})
                    return redirect('person:Dashboard')
                else:
                    return render(request, self.template_name, {'form': forms.LoginForm(), 'error': '1', 'msg': 'Incorrect Password'})
        except:
            return render(request, self.template_name, {'form': forms.LoginForm(), 'error': '1', 'msg': 'Incorrect Submission'})

class SignupView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': forms.SignupForm()})

    def post(self, request):
        try:
            form = forms.SignupForm(request.POST)
            if form.is_valid():
                db_name = utils.get_database_name()
                token = make_password(get_random_string(length = 16))
                password = make_password(form.cleaned_data['password'])
                r = utils.insert_user(db_name, form.cleaned_data['email'], password, token, 'U')
                if r == 201:
                    return render(request, self.template_name, {'form': forms.SignupForm(), 'success': '1', 'msg': 'Account created Successfully'})
                else:
                    return render(request, self.template_name, {'form': forms.SignupForm(), 'error': '1', 'msg': 'Network error. Try later.'})
            else:
                return render(request, self.template_name, {'form': form, 'error': '1', 'form_err': '1'})
        except Exception as e:
            return render(request, self.template_name, {'form': forms.SignupForm(), 'error': '1', 'msg': 'Incorrect Submission'})

class ForgotView(View):
    template_name = 'accounts/forgot.html'

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def get(self, request):
        return render(request, self.template_name, {'form': forms.ForgotForm()})

    def post(self, request):
        form = forms.ForgotForm(request.POST)
        if form.is_valid():
            user = self.get_object(form.cleaned_data['email'])
            user = user[0]
            token = get_random_string(length = 16)
            r = utils.update_user(user.db_name, user.email, token = make_password(token))
            if r == 200:
                mail.sendUserForgotMail(user.email, token)
                return render(request, self.template_name, {'form': forms.ForgotForm(), 'success': '1', 'msg': 'Please check your email for further instructions'})
            else:
                return render(request, self.template_name, {'form': forms.ForgotForm(), 'error': '1', 'msg': 'Network Error. Please try again later.'})
        else:
            return render(request, self.template_name, {'form': forms.ForgotForm(), 'error': '1', 'msg': 'Email is not registered'})

class PasswordResetView(View):
    template_name = 'accounts/reset.html'

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def get(self, request):
        user = self.get_object(request.GET.get('id'))
        if user.count() > 0:
            user = user[0]
            r = utils.get_user(user.db_name, user.email)
            if check_password(request.GET.get('token'), r.get('token')) == True:
                return render(request, self.template_name, {'form': forms.PasswordResetForm()})
            else:
                print('PAGE NOT FOUND')
        else:
            print('PAGE NOT FOUND')

    def post(self, request):
        form = forms.PasswordResetForm(request.POST)
        if form.is_valid():
            user = self.get_object(request.GET.get('id'))[0]
            token = make_password(get_random_string(length = 16))
            password = make_password(form.cleaned_data['password'])
            r = utils.update_user(user.db_name, user.email, token = token, password = password)
            if r == 200:
                return render(request, 'accounts/reset_done.html')
            else:
                return render(request, self.template_name, {'form': form, 'error': '1', 'msg': 'Network Error. Please try again later'})
        else:
            return render(request, self.template_name, {'form': form, 'form_err': '1'})
