from django.db.models.signals import post_save
from django.dispatch import receiver
from match_mate.match.models import Fixtures
from .models import Predictions


@receiver(post_save, sender=Fixtures)
def evaluate_predictions_on_fixture_update(sender, instance, **kwargs):
    """
    When a Fixture result is updated, re-evaluate all predictions linked to it.
    """
    if instance.actualHomeScore is not None and instance.actualAwayScore is not None:
        for prediction in instance.predictions.all():
            prediction.evaluate()
            
