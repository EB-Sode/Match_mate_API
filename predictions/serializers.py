from rest_framework import serializers
from .models import Predictions, MatchResult



# MATCH RESULT SERIALIZER
class MatchResultSerializer(serializers.ModelSerializer):
    fixture = serializers.StringRelatedField()  # Display fixture as a string
    outcome = serializers.CharField(source="get_outcome", read_only=True)

    class Meta:
        model = MatchResult
        fields = ['id', 'fixture', 'actual_home_score', 'actual_away_score', 'outcome']



#PREDICTION SERIALIZER
class PredictionSerializer(serializers.ModelSerializer):
    result = MatchResultSerializer(source="fixture.result", read_only=True)
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()

    class Meta:
        model = Predictions
        fields = ["id", "user", "fixture", "predicted_home_score", "predicted_away_score", "points_awarded", "home_team", "away_team", "result"]
        
        read_only_fields = ["points_awarded", 'user']

    def get_home_team(self, obj):
        return obj.fixture.home_team.name

    def get_away_team(self, obj):
        return obj.fixture.away_team.name

    def create(self, validated_data):
        prediction, created = Predictions.objects.update_or_create(
            user=validated_data["user"],
            fixture=validated_data["fixture"],
            defaults={
                "predicted_home_score": validated_data["predicted_home_score"],
                "predicted_away_score": validated_data["predicted_away_score"],
            },
        )
        return prediction