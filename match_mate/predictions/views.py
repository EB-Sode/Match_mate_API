from django.shortcuts import render
from .serializers import PredictionSerializer
from rest_framework.viewsets import ViewSet
from .models import Predictions

# Create your views here.

class PredictionViewSet(ViewSet):
    queryset = Predictions.objects.all()
    serializer_class = PredictionSerializer

    def get_queryset(self):
        """Only show the logged-in user's predictions"""
        return Predictions.objects.filter(user=self.request.user)
