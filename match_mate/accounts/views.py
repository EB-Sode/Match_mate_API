from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from .serializer import UserSerializer, RegisterUser, LeaderboardSerializer
from django.contrib.auth.models import User
from .models import UserStats

# Create your views here.
class RegisterView(generics.CreateAPIView):
    '''Handles registeration of users'''
    queryset = User.objects.all()
    serializer_class = RegisterUser

# Handles CRUD for users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LeaderboardView(generics.ListAPIView):
    '''Handles retrieval of the leaderboard'''
    queryset = UserStats.objects.all()
    serializer_class = LeaderboardSerializer