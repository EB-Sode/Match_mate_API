from rest_framework import serializers
from .models import Team, Fixtures, League

#LEAGUE SERIALIZER
class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'country']


#TEAM SERIALIZER 
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'league']

#  FIXTURES SERIALIZER
class FixtureSerializer(serializers.ModelSerializer):
    homeTeam = TeamSerializer(read_only=True)
    awayTeam = TeamSerializer(read_only=True)

    '''To allow creating fixtures by ID instead of nested team objects'''
    homeTeam_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source="homeTeam", write_only=True
    )
    awayTeam_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source="awayTeam", write_only=True
    )

    class Meta:
        model = Fixtures
        fields = [
            'id',
            'homeTeam', 'awayTeam',
            'homeTeam_id', 'awayTeam_id',
            'matchDate', 'actualHomeScore', 'actualAwayScore'
        ]
