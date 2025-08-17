from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Sum

# Create your models here.
class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    total_points = models.PositiveIntegerField(default=0)
    correct_predictions = models.PositiveIntegerField(default=0)


class Leaderboard(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leaderboard"
    )
    total_points = models.IntegerField(default=0)

    def update_points(self):
        total = self.user.predictions.aggregate(
            total=Sum('point_awarded')
        )['total'] or 0
        self.total_points = total
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.total_points} pts"