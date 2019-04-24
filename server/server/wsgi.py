"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from database import models, utils
import threading, time

def heartbeat():
    print('----------------------------------------------- HEARTBEAT ------------------------------------------------')
    S = utils.check_status()
    print(S)
    print('----------------------------------------------------------------------------------------------------------')
    for key in S:
        db = models.DatabaseDetails.objects.get(name = key)
        db.status = S[key]
        db.save()
    time.sleep(10)
    heartbeat()

heartbeat_thread = threading.Thread(target = heartbeat)
heartbeat_thread.start()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = get_wsgi_application()
