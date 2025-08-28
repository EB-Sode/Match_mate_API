from django.db import models
from django.conf import settings
from match.models import Fixtures
from django.db.models import Sum
from accounts.models import UserStats

# Create your models here.

#Store actual match results
class MatchResult(models.Model):
    fixture = models.OneToOneField(Fixtures, on_delete=models.CASCADE, related_name="result")
    actual_home_score = models.IntegerField()
    actual_away_score = models.IntegerField()

    def __str__(self):
        return f"Result: {self.fixture} → {self.actual_home_score}-{self.actual_away_score}"

    # def get_match_summary(self):
    #     return {
    #         "home_team": self.fixture.home_team,
    #         "away_team": self.fixture.away_team,
    #         "match_date": self.fixture.match_date_time,
    #         "actual_home_score": self.actual_home_score,
    #         "actual_away_score": self.actual_away_score,
    #         "outcome": self.get_outcome(),
    #     }
    
    def get_outcome(self):
        if self.actual_home_score > self.actual_away_score:
            return "HOME_WIN"
        elif self.actual_home_score < self.actual_away_score:
            return "AWAY_WIN"
        return "DRAW"
    

#Fixture predictions for all teams
class Predictions(models.Model):
    """Stores a user's prediction for a match fixture"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    fixture = models.ForeignKey(Fixtures, on_delete=models.CASCADE, related_name='predictions')
    points_awarded = models.PositiveIntegerField(default=0)
    predicted_home_score = models.PositiveIntegerField(null=True, blank=True)
    predicted_away_score = models.PositiveIntegerField(null=True, blank=True)


    class Meta:
        unique_together = ('user', 'fixture')  # prevent duplicate predictions

    def __str__(self):
        return f"{self.user.username} predict {self.fixture} and earn {self.points_awarded} points"
    
    def evaluate(self):
            # result is only available if the match has been played
        result = getattr(self.fixture, 'result', None)
        if result is None:
            return

        """Scoring system"""
        if (self.predicted_home_score == result.actual_home_score and
            self.predicted_away_score == result.actual_away_score):
            self.points_awarded = 3  # Exact scoreline correct

        # Correct outcome (win/draw/lose) & goal diff
        elif ((self.predicted_home_score - self.predicted_away_score) ==
              (result.actual_home_score - result.actual_away_score)):
            self.points_awarded = 2 

        # Just the right outcome (win/lose/draw)
        elif ((self.predicted_home_score > self.predicted_away_score and
               result.actual_home_score > result.actual_away_score) or
              (self.predicted_home_score < self.predicted_away_score and
               result.actual_home_score < result.actual_away_score) or
              (self.predicted_home_score == self.predicted_away_score and
               result.actual_home_score == result.actual_away_score)):
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
