from django.contrib import admin
from . import models

admin.site.register(models.DatabaseDetails)
admin.site.register(models.UserMetaData)
admin.site.register(models.ServiceMetaData)
admin.site.register(models.BookingMetaData)
