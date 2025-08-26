from rest_framework import serializers
from .models import Predictions

#PREDICTION SERIALIZER
class PredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Predictions
        fields = ["id", "user", "fixture", "predicted_home_score", "predicted_away_score", "points_awarded"]
        read_only_fields = ["points_awarded", 'user']

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