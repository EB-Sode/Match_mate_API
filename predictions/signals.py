from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MatchResult, Predictions
            
@receiver(post_save, sender=MatchResult)
def evaluate_predictions_on_fixture_update(sender, instance, **kwargs):
    """
    When a Fixture result is updated, re-evaluate all predictions linked to it.
    """
    # Make sure the result has actual scores
    if instance.actual_home_score is not None and instance.actual_away_score is not None:
        # Access predictions via the fixture
        for prediction in instance.fixture.predictions.all():
            prediction.evaluate()  # assuming your Predictions model has an evaluate() method