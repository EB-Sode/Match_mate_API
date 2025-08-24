from django.db import models



# Create your models here.

#Leagues where teams are participating
class League(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

#Create teams for match predictions
class Team(models.Model):
    name= models.CharField(max_length=100)
    logo = models.ImageField(upload_to="team_logos/", null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')

#Create team fixtures
class Fixtures(models.Model):
    '''Games to be played and predicted'''
    homeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    awayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    matchDate = models.DateField()
    STATUS_CHOICES = (
        ("upcoming", "Upcoming"),
        ("live", "Live"),
        ("finished", "Finished"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")


    def __str__(self):
        return f"{self.homeTeam} vs {self.awayTeam} on {self.matchDate}"

class MatchResult(models.Model):
    fixture = models.OneToOneField(Fixtures, on_delete=models.CASCADE, related_name="result")
    actual_home_score = models.IntegerField()
    actual_away_score = models.IntegerField()

    def __str__(self):
        return f"Result: {self.fixture} → {self.actual_home_score}-{self.actual_away_score}"

    def get_match_summary(self):
        return {
            "home_team": self.fixture.homeTeam,
            "away_team": self.fixture.awayTeam,
            "match_date": self.fixture.matchDate,
            "actual_home_score": self.actual_home_score,
            "actual_away_score": self.actual_away_score,
        }