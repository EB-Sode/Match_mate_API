from django.db import models
from django.conf import settings
from match.models import MatchResult
from django.db.models import Sum
from accounts.models import UserStats

# Create your models here.

#Fixture predictions for all teams
class Predictions(models.Model):
    """Stores a user's prediction for a match fixture"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    fixture = models.ForeignKey(MatchResult, on_delete=models.CASCADE, related_name='predictions')
    points_awarded = models.PositiveIntegerField(default=0)
    predicted_home_score = models.PositiveIntegerField(null=True, blank=True)
    predicted_away_score = models.PositiveIntegerField(null=True, blank=True)


    class Meta:
        unique_together = ('user', 'fixture')  # ✅ prevent duplicate predictions

    def __str__(self):
        return f"{self.user.username} predict {self.fixture} and earn {self.points_awarded} points"
    
    def evaluate(self):
        """Compare prediction with result and assign points."""
        #skip when match is not yet played
        if self.fixture.actual_home_score is None or self.fixture.actual_away_score is None:
            return

        # scoring system
        if (self.predicted_home_score == self.fixture.actual_home_score and
            self.predicted_away_score == self.fixture.actual_away_score):
            self.points_awarded = 3  # Exact scoreline correct

        # Correct outcome (win/draw/lose) & goal diff
        elif ((self.predicted_home_score - self.predicted_away_score) ==
              (self.fixture.actual_home_score - self.fixture.actual_away_score)):
            self.points_awarded = 2 

        # Just the right outcome (win/lose/draw)
        elif ((self.predicted_home_score > self.predicted_away_score and
               self.fixture.actual_home_score > self.fixture.actual_away_score) or
              (self.predicted_home_score < self.predicted_away_score and
               self.fixture.actual_home_score < self.fixture.actual_away_score) or
              (self.predicted_home_score == self.predicted_away_score and
               self.fixture.actual_home_score == self.fixture.actual_away_score)):
            self.points_awarded = 1

        # Totally wrong
        else:
            self.points_awarded = 0

        self.save()

        # Update user statistics
        self.update_user_stats()

    def update_user_stats(self):
        """Update or create UserStats for this user"""
        
        stats, created = UserStats.objects.get_or_create(user=self.user)

        # update totals
        stats.total_points = self.user.predictions.aggregate(total=Sum("points_awarded"))["total"] or 0
        stats.correct_predictions = self.user.predictions.filter(points_awarded__gt=0).count()
        stats.save()
