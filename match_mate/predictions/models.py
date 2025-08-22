from django.db import models
from django.conf import settings
from match.models import Fixtures
from django.db.models import Sum
from accounts.models import UserStats

# Create your models here.

#Fixture predictions for all teams
class Predictions(models.Model):
    """Stores a user's prediction for a match fixture"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    fixture = models.ForeignKey(Fixtures, on_delete=models.CASCADE, related_name= 'predictions')
    points_awarded = models.PositiveIntegerField(default=0)
    predictedHomeScore = models.PositiveIntegerField(null=True, blank=True)
    predictedAwayScore = models.PositiveIntegerField(null=True, blank=True)

    # predicted_result = models.CharField(
    #     max_length=10,
    #     choices=[("home", "Home Win"), ("away", "Away Win"), ("draw", "Draw")],
    #     null=True, blank=True
    # )  
 
    class Meta:
        unique_together = ('user', 'fixture')  # ✅ prevent duplicate predictions

    def __str__(self):
        return f"{self.user.username} predict {self.fixture} and earn {self.points_awarded} points"
    
    def evaluate(self):
        """Compare prediction with actual result and assign points."""
        #skip when match is not yet played
        if self.fixture.actualHomeScore is None or self.fixture.actualAwayScore is None:
            return

        # scoring system
        if (self.predictedHomeScore == self.fixture.actualHomeScore and
            self.predictedAwayScore == self.fixture.actualAwayScore):
            self.points_awarded = 3  # Exact scoreline correct

        # Correct outcome (win/draw/lose) & goal diff
        elif ((self.predictedHomeScore - self.predictedAwayScore) ==
              (self.fixture.actualHomeScore - self.fixture.actualAwayScore)):
            self.points_awarded = 2 

        # Just the right outcome (win/lose/draw)    
        elif ((self.predictedHomeScore > self.predictedAwayScore and 
               self.fixture.actualHomeScore > self.fixture.actualAwayScore) or
              (self.predictedHomeScore < self.predictedAwayScore and 
               self.fixture.actualHomeScore < self.fixture.actualAwayScore) or
              (self.predictedHomeScore == self.predictedAwayScore and 
               self.fixture.actualHomeScore == self.fixture.actualAwayScore)):
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
