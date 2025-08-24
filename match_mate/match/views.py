
from .serializers import TeamSerializer, LeagueSerializer, FixtureSerializer
from rest_framework import viewsets, permissions
from .models import Team, League, Fixtures
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .utils import import_fixtures


# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['id']

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['name']

class FixtureViewSet(viewsets.ModelViewSet):
    queryset = Fixtures.objects.all()
    serializer_class = FixtureSerializer
    permission_classes = [permissions.AllowAny]
    filtering_fields = ['league', 'matchdate']
    ordering_fields = ['matchdate']

    '''Import fixtures before listing'''
    def list(self, request, *args, **kwargs):
        # Call your util function before returning fixtures
        import_fixtures()
        return super().list(request, *args, **kwargs)

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def import_fixtures_view(request):
#     try:
#         imported_count = import_fixtures()
#         return Response({"message": f"{imported_count} fixtures imported successfully"})
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

