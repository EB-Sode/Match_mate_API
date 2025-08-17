from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .serializer import UserSerializer, RegisterUser
from django.contrib.auth.models import User

# Create your views here.
class RegisterView(generics.CreateAPIView):
    '''Handles registeration of users'''
    queryset = User.objects.all()
    serializer_class = RegisterUser

# Handles CRUD for users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer