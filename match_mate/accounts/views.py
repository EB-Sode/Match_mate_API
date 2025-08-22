
from rest_framework import generics
from rest_framework import viewsets, permissions
from .serializer import UserSerializer, RegisterUser, LeaderboardSerializer
from django.contrib.auth.models import User
from .models import UserStats
from match.permissions import IsOwnerOrReadOnly

# Create your views here.
class RegisterView(generics.CreateAPIView):
    '''Handles registeration of users'''
    queryset = User.objects.all()
    serializer_class = RegisterUser
    permission_classes = [permissions.AllowAny]

# Handles CRUD for profile management
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Handles retrieval of the leaderboard
class LeaderboardView(generics.ListAPIView):
    '''Handles retrieval of the leaderboard'''
    queryset = UserStats.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsOwnerOrReadOnly]