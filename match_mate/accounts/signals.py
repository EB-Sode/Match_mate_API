# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Leaderboard

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_leaderboard(sender, instance, created, **kwargs):
    if created:
        Leaderboard.objects.create(user=instance)
