from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, LeagueViewSet, FixtureViewSet
from predictions.views import PredictionViewSet

#Create routers
router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'fixtures', FixtureViewSet)
router.register(r'predictions', PredictionViewSet, basename='prediction')

urlpatterns = [
    path('', include(router.urls)),
]
