from django.db import models

class User(models.Model):
    USER_TYPES = (
        ('U', 'Standard User'),
        ('A', 'Admin'),
        ('S', 'Service Provider'),
    )
    email = models.EmailField(primary_key = True, null = False, max_length = 100)
    password = models.CharField(max_length = 500, null = False)
    token = models.CharField(max_length = 500, null = False)
    type = models.CharField(max_length = 1, choices = USER_TYPES, null = False)
    activated = models.BooleanField(default = False)

    def __str__(self):
        return self.email
