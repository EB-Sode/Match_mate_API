from django.shortcuts import render
from .serializers import PredictionSerializer, MatchResultSerializer
from rest_framework.viewsets import ViewSet
from .models import Predictions, MatchResult
from rest_framework import permissions, viewsets
from match.permissions import IsOwnerOrReadOnly
from rest_framework import filters

# Create your views here.
class MatchResultViewSet(viewsets.ModelViewSet):
    queryset = MatchResult.objects.all()
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Predictions.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PredictionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["fixture__home_team__name", "fixture__away_team__name"]  # 🔍 filter by fixtures
    ordering_fields = ["fixture__matchdate"]

    def get_queryset(self):
        """Only show the logged-in user's predictions"""
        return Predictions.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically assign logged-in user
        serializer.save(user=self.request.user)
