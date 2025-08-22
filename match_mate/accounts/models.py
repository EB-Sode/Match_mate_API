from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class UserStats(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stats"
    )
    total_points = models.PositiveIntegerField(default=0)
    correct_predictions = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.total_points} pts"
