from django.core.mail import EmailMessage
from django.utils import http
from django.urls import reverse

WEBSITE = '127.0.0.1:9000'

def sendUserRegisteredMail(name, email, token):
    Subject = 'Welcome to MCQTS'
    Body = 'Hello, ' + name + '<br> <br> ' + 'Thankyou for registering at MCQTS. Your new account has been created. You may login after activating your account. Click the link to activate your account: <br>'
    Body += ' <br> Link: ' + 'http://localhost:8000' + reverse('accounts:activate') + '?id='+ http.urlquote_plus(email) +'&token='+ http.urlquote_plus(token)
    Body += '<br> <br> <b> This is an automatically generated email. Do not reply back. </b> <br> <br>'
    Body += 'Regards <br> MCQTS'
    email = EmailMessage(Subject, Body, to=[email,])
    email.content_subtype = "html"
    return email.send()

def sendUserForgotMail(email, token):
    Subject = 'Login Details - Travel Agency'
    Body = 'Hello, <br> <br> ' + 'You had requested to reset your password at Online Travel Agency.'
    Body += ' <br> To reset your password, click on the link: ' + WEBSITE + reverse('accounts:Reset') + '?id='+ http.urlquote_plus(email) +'&token='+ http.urlquote_plus(token)
    Body += '<br> <br> <b> This is an automatically generated email. Do not reply back. </b> <br> <br>'
    Body += 'Regards <br> Travel Agency'
    email = EmailMessage(Subject, Body, to=[email,])
    email.content_subtype = "html"
    return email.send()
