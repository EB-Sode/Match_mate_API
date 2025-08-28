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
    logo = models.ImageField(upload_to="media/team_logos/", null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')

#Create team fixtures
class Fixtures(models.Model):
    '''Games to be played and predicted'''
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_team')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_team')
    match_date_time = models.DateTimeField()
    status = models.CharField(max_length=20, default="upcoming")
    external_id = models.IntegerField(unique=True, null= True)  # Store the external API's fixture ID

    class Meta:
        ordering = ['match_date_time']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.match_date_time}"

    