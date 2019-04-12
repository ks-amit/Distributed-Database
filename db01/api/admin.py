from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('password', 'token', 'email', )

admin.site.register(models.User)
admin.site.register(models.BusService)
admin.site.register(models.HotelService)
admin.site.register(models.HotelBooking)
