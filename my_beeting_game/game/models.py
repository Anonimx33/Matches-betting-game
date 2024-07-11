from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

class Team(models.Model):
    team_name = models.CharField(max_length=255)

    def __str__(self):
        return self.team_name

class Match(models.Model):
    teams = models.ManyToManyField(Team)
    goals_1 = models.IntegerField(default=0)
    goals_2 = models.IntegerField(default=0)
    
    def clean(self):
        if self.teams.count() != 2:
            raise ValidationError('Match can be played only by 2 teams')
        
    def __str__(self):
        teams = self.teams.all()
        return f"{teams[0]} - {teams[1]}: {self.goals_1}:{self.goals_2}"

class Group(models.Model):
    group_name = models.CharField(max_length=1)
    teams = models.ManyToManyField(Team)
    matches = models.ManyToManyField(Match)

    def __str__(self):
        return self.group_name

    def clean(self):
        if self.teams.count() > 4:
            raise ValidationError('Group can only have 4 teams')
    

    
    