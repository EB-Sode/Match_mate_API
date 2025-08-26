from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchResult
from predictions.models import Prediction  # import Prediction model

@receiver(post_save, sender=MatchResult)
def update_predictions_on_result_save(sender, instance, created, **kwargs):
    """ Whenever a MatchResult is saved (created or updated), 
        re-evaluate all predictions for that fixture. """
    fixture = instance.fixture  # MatchResult -> Fixture
    predictions = fixture.predictions.all()  # Fixture -> related Predictions

    for prediction in predictions:
        prediction.evaluate()