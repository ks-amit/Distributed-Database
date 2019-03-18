from rest_framework import serializers
from .models import User, BusService

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password', 'email', 'type', 'token', 'activated', )

class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusService
        fields = ('id', 'name', 'route', 'timing', 'price', 'bus_number', 'is_ready', )
