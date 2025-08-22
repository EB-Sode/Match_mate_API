from django.shortcuts import render
from .serializers import PredictionSerializer
from rest_framework.viewsets import ViewSet
from .models import Predictions
from rest_framework import permissions
from match.permissions import IsOwnerOrReadOnly
from rest_framework import filters

# Create your views here.

class PredictionViewSet(ViewSet):
    queryset = Predictions.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PredictionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["fixtures", "content"]  # 🔍 filter by fixtures
    ordering_fields = ["fixtures"]

    def get_queryset(self):
        """Only show the logged-in user's predictions"""
        return Predictions.objects.filter(user=self.request.user)
