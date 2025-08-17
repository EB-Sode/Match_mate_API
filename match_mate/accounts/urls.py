from .views import RegisterView, UserViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

#routers for CRUD operations here
router = DefaultRouter()
router.register(r'users', UserViewSet, basename = 'user')

#urls here
urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),

    #Include routes
    path('', include(router.urls)),
]