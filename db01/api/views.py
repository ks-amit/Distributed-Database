from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, BusService
from .serializers import UserSerializer, BusSerializer
from rest_framework import status

class UserList(APIView):

    def get(self, request, format = None):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

class GetUser(APIView):

    def get_object(self, email):
        return User.objects.filter(email = email)

    def get(self, request, format = None):
        user = self.get_object(request.data.get('email'))
        if not user:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserSerializer(user, many = True)
            return Response(serializer.data)

class InsertUser(APIView):

    def get_object(self, email):
        return User.objects.filter(email = email)

    def post(self, request, format = None):
        user = self.get_object(request.data.get('email'))
        if not user:
            try:
                new_user = User(email = request.data.get('email'),
                                password = request.data.get('password'),
                                token = request.data.get('token'),
                                type = request.data.get('type'))

                new_user.full_clean()
                new_user.save()
                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):

    def get_object(self, email):
        return User.objects.filter(email = email)

    def post(self, request, format = None):
        user = self.get_object(request.data.get('email'))
        if not user:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            user = user[0]
            try:
                if request.data.get('token') != None:
                    user.token = request.data.get('token')
                if request.data.get('password') != None:
                    user.password = request.data.get('password')
                if request.data.get('type') != None:
                    user.type = request.data.get('type')
                user.full_clean()
                user.save()
                return Response(status = status.HTTP_200_OK)
            except:
                return Response(status = status.HTTP_400_BAD_REQUEST)

class BusServiceList(APIView):

    def get(self, request, format = None):
        services = BusService.objects.all()
        serializer = BusSerializer(services, many = True)
        return Response(serializer.data)

class NewBusService(APIView):

    def get_object(self, id):
        return BusService.objects.filter(id = id)

    def post(self, request, format = None):
        service = self.get_object(request.data.get('id'))
        if not service:
            try:
                new_service = BusService(   id = request.data.get('id'),
                                            name = request.data.get('name'))
                new_service.full_clean()
                print('CLEANED')
                new_service.save()
                return Response(status = status.HTTP_201_CREATED)
            except Exception as e:
                print('EXCEPTION THROW')
                print(e)
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
