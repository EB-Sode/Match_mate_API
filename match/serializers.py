from rest_framework import serializers

# from predictions.serializers import PredictionSerializer
from .models import Team, Fixtures, League
from predictions.serializers import MatchResultSerializer

#LEAGUE SERIALIZER
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['name']

#TEAM SERIALIZER 
class TeamSerializer(serializers.ModelSerializer):
    league = LeagueSerializer()

    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'league']

#  FIXTURES SERIALIZER
class FixtureSerializer(serializers.ModelSerializer):
    result = MatchResultSerializer(read_only=True)
    home_team = serializers.SlugRelatedField(slug_field="name", queryset=Team.objects.all())
    away_team = serializers.SlugRelatedField(slug_field="name", queryset=Team.objects.all())
    # league = serializers.SlugRelatedField(slug_field="name", queryset=League.objects.all())

    '''To allow creating fixtures by ID instead of nested team objects'''
    home_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="home_team", write_only=True)
    away_team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="away_team", write_only=True)
    # league_id = serializers.PrimaryKeyRelatedField(queryset=League.objects.all(), source="league", write_only=True

    class Meta:
        model = Fixtures
        fields = ['id', 'home_team', 'away_team', 'home_team_id', 'away_team_id', 'match_date_time', 'status', 'result']

