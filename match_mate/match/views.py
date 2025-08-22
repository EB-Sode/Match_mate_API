from django.shortcuts import render
from .serializers import TeamSerializer, LeagueSerializer, FixtureSerializer
from rest_framework import viewsets, permissions
from .models import Team, League, Fixtures
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [permissions.AllowAny]

class FixtureViewSet(viewsets.ModelViewSet):
    queryset = Fixtures.objects.all()
    serializer_class = FixtureSerializer
    permission_classes = [permissions.AllowAny]
