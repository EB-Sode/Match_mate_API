from django.db import models



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
