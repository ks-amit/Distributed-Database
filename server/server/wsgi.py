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
        if(S[key] == 1):
            pending_updates = models.PendingUpdates.objects.filter(db_name = db.name).order_by('timestamp')
            while pending_updates.count() > 0:
                for update in pending_updates:
                    try:
                        r = utils.perform_update(update)
                        if r == 200 or r == 201:
                            update.delete()
                    except Exception as e:
                        print(e)
                        continue

                pending_updates = models.PendingUpdates.objects.filter(db_name = db.name).order_by('timestamp')

        db.status = S[key]
        db.save()
    wait_time = int(models.HeartBeatRate.objects.all()[0].rate)
    time.sleep(wait_time)
    heartbeat()

heartbeat_thread = threading.Thread(target = heartbeat)
heartbeat_thread.start()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = get_wsgi_application()
