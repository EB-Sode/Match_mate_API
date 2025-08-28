
from .serializers import TeamSerializer, LeagueSerializer, FixtureSerializer
from rest_framework import viewsets, filters
from .models import Team, League, Fixtures
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import import_fixtures
from django.views import generic
from django.db.models import Q
from django.urls import reverse_lazy as reverse
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'league']

class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['name']

class FixtureViewSet(viewsets.ModelViewSet):
    queryset = Fixtures.objects.all()
    serializer_class = FixtureSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']  # exact match filters
    search_fields = ['home_team__name', 'away_team__name']  # text search
    ordering_fields = ['match_date_time', 'status']
    ordering = ['match_date_time']  # default ordering

    # def get_queryset(self):
    #     status = self.request.query_params.get('status')
    #     team = self.request.query_params.get('team')
    #     queryset = super().get_queryset()

    #     if team:
    #         queryset = queryset.filter(Q(home_team__name__icontains=team) | Q(away_team__name__icontains=team))
        
    #     if status:
    #        queryset = queryset.filter(status=status)
        
    #     return queryset.order_by('match_date_time')

    # def list(self, request, *args, **kwargs):
    #     '''Import fixtures before listing'''
    #    
    #     import_fixtures() #run via cron job
    #     return super().list(request, *args, **kwargs)

# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def import_fixtures_view(request):
#     try:
#         imported_count = import_fixtures()
#         return Response({"message": f"{imported_count} fixtures imported successfully"})
#     except Exception as e:
#         return Response({"error": str(e)}, status=500)

class TeamEdit(generic.UpdateView):
    model = Team
    fields = ['name', 'logo', 'league']
    template_name = 'team_edit.html'
    success_url = "/api/teams/"
