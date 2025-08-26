
from .serializers import TeamSerializer, LeagueSerializer, FixtureSerializer, MatchResultSerializer
from rest_framework import viewsets
from .models import Team, League, Fixtures, MatchResult
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import import_fixtures
from django.views import generic
from django.urls import reverse_lazy as reverse


# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['id']

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['name']

class FixtureViewSet(viewsets.ModelViewSet):
    queryset = Fixtures.objects.all()
    serializer_class = FixtureSerializer
    permission_classes = [AllowAny]
    filtering_fields = ['league', 'matchdate']
    ordering_fields = ['matchdate']

    '''Import fixtures before listing'''
    def list(self, request, *args, **kwargs):
        # Call your util function before returning fixtures
        import_fixtures() #run via cron job 
        return super().list(request, *args, **kwargs)

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def import_fixtures_view(request):
#     try:
#         imported_count = import_fixtures()
#         return Response({"message": f"{imported_count} fixtures imported successfully"})
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)


class MatchResultViewSet(viewsets.ModelViewSet):
    queryset = MatchResult.objects.all()
    serializer_class = MatchResultSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users

class TeamEdit(generic.UpdateView):
    model = Team
    fields = ['name', 'logo', 'league']
    template_name = 'team_edit.html'
    success_url = "/api/teams/"
