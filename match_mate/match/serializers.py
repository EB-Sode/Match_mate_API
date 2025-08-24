from rest_framework import serializers

from predictions.models import Predictions
from .models import Team, Fixtures, League, MatchResult

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
    homeTeam = serializers.SlugRelatedField(slug_field="name", queryset=Team.objects.all())
    awayTeam = serializers.SlugRelatedField(slug_field="name", queryset=Team.objects.all())
    # league = serializers.SlugRelatedField(slug_field="name", queryset=League.objects.all())

    '''To allow creating fixtures by ID instead of nested team objects'''
    homeTeam_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="homeTeam", write_only=True)
    awayTeam_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source="awayTeam", write_only=True)
    # league_id = serializers.PrimaryKeyRelatedField(queryset=League.objects.all(), source="league", write_only=True

    class Meta:
        model = Fixtures
        fields = [
            'id',
            'homeTeam', 'awayTeam',
            'homeTeam_id', 'awayTeam_id',
            'matchDate', 'actual_home_score', 'actual_away_score'
        ]

class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchResult
        fields = "__all__"

    def create(self, validated_data):
        # Save result normally
        result = super().create(validated_data)

        # After result is created → update predictions
        for prediction in result.fixture.predictions.all():
            prediction.evaluate()
        return result