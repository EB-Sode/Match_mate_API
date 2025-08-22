from .views import RegisterView, UserViewSet, LeaderboardView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#routers for CRUD operations here
router = DefaultRouter()
router.register(r'users', UserViewSet, basename = 'user')

#urls here
urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    #Include routes
    path('', include(router.urls)),
]