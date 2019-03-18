from django import forms
from database import models
from django.core import validators

class LoginForm(forms.Form):
    email = forms.EmailField(max_length = 100, required = True)
    password = forms.CharField(max_length = 100, required = True)

class SignupForm(forms.Form):
    email = forms.EmailField(max_length = 100, required = True)
    password = forms.CharField(max_length = 100, required = True)
    password_cnf = forms.CharField(max_length = 100, required = True)

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            v = validators.validate_email(email)
        except:
            raise forms.ValidationError("Enter a valid email address")

        try:
            user = self.get_object(email)
            if user.count() > 0:
                raise forms.ValidationError("User already exists")
            else:
                return email
        except Exception as e:
            raise e

    def clean_password_cnf(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password_cnf']
        if len(pass1) == 0 or len(pass2) == 0:
            raise forms.ValidationError("Fields cannot be empty")
        elif pass1 != pass2:
            raise forms.ValidationError("Passwords do not match")
        else:
            return pass1

class ForgotForm(forms.Form):
    email = forms.EmailField(max_length = 100, required = True)

    def get_object(self, email):
        return models.UserMetaData.objects.filter(email = email)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = self.get_object(email)
        if user.count() > 0:
            return email
        else:
            raise forms.ValidationError("Email not registered")

class PasswordResetForm(forms.Form):
    password = forms.CharField(max_length = 100, required = True)
    password_cnf = forms.CharField(max_length = 100, required = True)

    def clean_password_cnf(self):
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['password_cnf']
        if len(pass1) == 0 or len(pass2) == 0:
            raise forms.ValidationError("Fields cannot be empty")
        elif pass1 != pass2:
            raise forms.ValidationError("Passwords do not match")
        else:
            return pass1
