from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class DatabaseDetails(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    ip_addr = models.CharField(max_length = 20, null = False)
    port = models.CharField(max_length = 8, null = False)
    size = models.IntegerField(default = 0)
    status = models.CharField(max_length = 20, default = '', null = True)

    def __str__(self):
        return self.name

class HeartBeatRate(models.Model):
    rate = models.IntegerField()

class UserMetaData(models.Model):
    email = models.EmailField(max_length = 100, primary_key = True)
    db_name = models.CharField(max_length = 50)
    db_name_0 = models.CharField(max_length = 50, default = '')
    db_name_1 = models.CharField(max_length = 50, default = '')
    db_name_2 = models.CharField(max_length = 50, default = '')

    def __str__(self):
        return self.email

class ServiceMetaData(models.Model):

    def default_array_field():
        return list([])

    CHOICES = ( ('B', 'Bus'),
                ('H', 'Hotel'),)
    id = models.CharField(primary_key = True, max_length = 64, null = False)
    name = models.CharField(max_length = 100, null = False)
    type = models.CharField(max_length = 1, choices = CHOICES, null = False)
    db_name = models.CharField(max_length = 50, null = False)
    db_name_0 = models.CharField(max_length = 50, default = '')
    db_name_1 = models.CharField(max_length = 50, default = '')
    db_name_2 = models.CharField(max_length = 50, default = '')
    provider = ArrayField(models.CharField(max_length = 100), default = default_array_field)
    capacity = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class BookingMetaData(models.Model):

    CHOICES = ( ('B', 'Bus'),
                ('H', 'Hotel'),)
    id = models.CharField(primary_key = True, max_length = 64, null = False)
    type = models.CharField(max_length = 1, choices = CHOICES, null = False)
    db_name = models.CharField(max_length = 50, null = False)
    db_name_0 = models.CharField(max_length = 20, default = '')
    db_name_1 = models.CharField(max_length = 20, default = '')
    db_name_2 = models.CharField(max_length = 20, default = '')
    start_date = models.DateField()

    def __str__(self):
        return self.id

class PendingUpdates(models.Model):

    CHOICES = ( ('POST', 'POST'),
                ('GET', 'GET'),
                ('PUT', 'PUT'),)

    def default_string_array():
        return list([])

    data_string_keys = ArrayField(models.CharField(max_length = 50), default = default_string_array)
    data_string_values = ArrayField(models.CharField(max_length = 2000), default = default_string_array)
    data_time_keys = ArrayField(models.CharField(max_length = 50), default = default_string_array)
    data_time_values = ArrayField(models.TimeField(), default = default_string_array)
    data_date_keys = ArrayField(models.CharField(max_length = 50), default = default_string_array)
    data_date_values = ArrayField(models.DateField(), default = default_string_array)
    data_boolean_keys =  ArrayField(models.CharField(max_length = 50), default = default_string_array)
    data_boolean_values =  ArrayField(models.BooleanField(), default = default_string_array)
    data_int_keys =  ArrayField(models.CharField(max_length = 50), default = default_string_array)
    data_int_values =  ArrayField(models.IntegerField(), default = default_string_array)
    addr = models.CharField(max_length = 100)
    db_name = models.CharField(max_length = 20, default = '')
    type = models.CharField(max_length = 4, choices = CHOICES)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.addr
