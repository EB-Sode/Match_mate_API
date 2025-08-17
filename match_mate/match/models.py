from django.db import models
from django.conf import settings


# Create your models here.

#League where teams are participating
class League(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

#Create teams for match predictions
class Team(models.Model):
    name= models.CharField(max_length=100)
    logo = models.ImageField(upload_to="team_logos/", null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='league')
    
#Create team fixtures
class Fixtures(models.Model):
    '''Games to be played and predicted'''
    homeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    awayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    matchDate = models.DateField()
    actualHomeScore = models.PositiveIntegerField()
    actualAwayScore = models.PositiveIntegerField()
    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("finished", "Finished"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")


    def __str__(self):
        return f"{self.homeTeam} vs {self.awayTeam} on {self.matchDate}"

    def get_match_summary(self):
        return {
            "home_team": self.homeTeam,
            "away_team": self.awayTeam,
            "match_date": self.matchDate,
            "actual_home_score": self.actualHomeScore,
            "actual_away_score": self.actualAwayScore,
        }

#Fixture predictions for all teams
class Predictions(models.Model):
    """Stores a user's prediction for a match fixture"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictor')
    fixture = models.ForeignKey(Fixtures, on_delete=models.CASCADE, related_name= 'predict')
    pointAwarded = models.PositiveIntegerField(default=0)
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
        return f"{self.user.username} predict {self.fixture} and earn points"
    
    def evaluate(self):
        """Compare prediction with actual result and assign points."""
        #skip when match is not yet played
        if self.fixture.actualHomeScore is None or self.fixture.actualAwayScore is None:
            return

        # scoring system
        if (self.predictedHomeScore == self.fixture.actualHomeScore and
            self.predictedAwayScore == self.fixture.actualAwayScore):
            self.pointAwarded = 3  # Exact scoreline correct

        # Correct outcome (win/draw/lose) & goal diff
        elif ((self.predictedHomeScore - self.predictedAwayScore) ==
              (self.fixture.actualHomeScore - self.fixture.actualAwayScore)):
            self.pointAwarded = 2 

        # Just the right outcome (win/lose/draw)    
        elif ((self.predictedHomeScore > self.predictedAwayScore and 
               self.fixture.actualHomeScore > self.fixture.actualAwayScore) or
              (self.predictedHomeScore < self.predictedAwayScore and 
               self.fixture.actualHomeScore < self.fixture.actualAwayScore) or
              (self.predictedHomeScore == self.predictedAwayScore and 
               self.fixture.actualHomeScore == self.fixture.actualAwayScore)):
            self.pointAwarded = 1  

        # Totally wrong
        else:
            self.pointAwarded = 0  

        self.save()



