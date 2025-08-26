from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, LeagueViewSet, FixtureViewSet, MatchResultViewSet, TeamEdit
from predictions.views import PredictionViewSet

app_name = 'match'

#Create routers
router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'leagues', LeagueViewSet)
router.register(r'fixtures', FixtureViewSet)
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'results', MatchResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
    path('team/<int:pk>/edit/', TeamEdit.as_view(), name='team_edit'),
]