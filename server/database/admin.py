from django.contrib import admin
from . import models

class PendingUpdatesAdmin(admin.ModelAdmin):
    fields = ('addr', 'type', 'timestamp', 'db_name', 'data_string_keys', 'data_string_values', 'data_time_keys', 'data_time_values', 'data_date_keys', 'data_date_values', 'data_boolean_keys', 'data_boolean_values', 'data_int_keys', 'data_int_values',)
    readonly_fields = ('timestamp',)

admin.site.register(models.DatabaseDetails)
admin.site.register(models.UserMetaData)
admin.site.register(models.ServiceMetaData)
admin.site.register(models.BookingMetaData)
admin.site.register(models.HeartBeatRate)
admin.site.register(models.PendingUpdates, PendingUpdatesAdmin)
