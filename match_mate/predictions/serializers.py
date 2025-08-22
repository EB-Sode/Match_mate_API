from rest_framework import serializers
from .models import Predictions

#PREDICTION SERIALIZER
class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = [
            "id",
            "user",
            "fixture",
            "fixtures_id",
            "predictedHomeScore",
            "predictedAwayScore",
            "points_awarded",
        ]
    
    read_only_fields = ["points_awarded"]

    def create(self, validated_data):
        prediction, created = Predictions.objects.update_or_create(
            user=validated_data["user"],
            fixture=validated_data["fixture"],
            defaults={
                "predictedHomeScore": validated_data["predictedHomeScore"],
                "predictedAwayScore": validated_data["predictedAwayScore"],
            },
        )
        return prediction