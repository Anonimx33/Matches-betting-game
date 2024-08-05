from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.utils import timezone

class Team(models.Model):
    OPTION_CHOICES = [(i, str(i)) for i in range(4)]
    team_name = models.CharField(max_length=255)
    matches_played = models.PositiveIntegerField(default=0, choices=OPTION_CHOICES)
    wins = models.PositiveIntegerField(default=0, choices=OPTION_CHOICES)
    draws = models.PositiveIntegerField(default=0, choices=OPTION_CHOICES)
    loses = models.PositiveIntegerField(default=0, choices=OPTION_CHOICES)
    goals_scored = models.PositiveIntegerField(default=0)
    goals_lost = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.team_name

class Match(models.Model):
    teams = models.ManyToManyField(Team)
    goals_1 = models.PositiveIntegerField(default=0)
    goals_2 = models.PositiveIntegerField(default=0)
    match_date = models.DateTimeField(default=timezone.now)
    previous_goals_1 = models.PositiveIntegerField(default=0, editable=False)
    previous_goals_2 = models.PositiveIntegerField(default=0, editable=False)
    
    def clean(self):
        if self.teams.count() != 2:
            raise ValidationError('Match can be played only by 2 teams')
                       
    def __str__(self):
        teams = self.teams.all()
        date = self.match_date.strftime("%Y-%m-%d %H:%M")
        if len(teams) < 2:
            return "Invalid match: not enough teams"
        return f"{date}: {teams[0]} - {teams[1]}: {self.goals_1}:{self.goals_2}"

def create_matches(group):
    teams = list(group.teams.all().order_by('-points', '-wins', '-goals_scored', 'team_name'))
    
    if len(teams) != 4:
        print("Nie ma dokładnie 4 zespołów w grupie.")
        return  # Nie twórz meczów, jeśli nie ma 4 zespołów
    
    # Wyczyść istniejące mecze przed dodaniem nowych
    group.matches.clear()

    matches = [
        (teams[0], teams[1]),
        (teams[2], teams[3]),
        (teams[0], teams[2]),
        (teams[1], teams[3]),
        (teams[0], teams[3]),
        (teams[1], teams[2]),
    ]
    
    for team1, team2 in matches:
        match = Match.objects.create()
        match.teams.set([team1, team2])
        match.save()  # Save to ensure match is saved to the database
        group.matches.add(match)  # Add match to the group's matches
        print(f"Utworzono mecz: {team1} vs {team2}")

def update_teams(match, reset=False):
    teams = match.teams.all()
    if len(teams) < 2:
        return
    team1, team2 = teams[0], teams[1]
    if reset:
        team1.goals_scored -= match.previous_goals_1
        team1.goals_lost -= match.previous_goals_2
        team2.goals_scored -= match.previous_goals_2
        team2.goals_lost -= match.previous_goals_1
        team1.matches_played -= 1
        team2.matches_played -= 1
        # Sprawdź, czy wartości są w odpowiednim zakresie
        if team1.matches_played < 0:
            team1.matches_played = 0
        if team2.matches_played < 0:
            team2.matches_played = 0
        if match.previous_goals_1 > match.previous_goals_2:
            team1.wins -= 1
            team1.points -= 3
            team2.loses -= 1
        elif match.previous_goals_1 < match.previous_goals_2:
            team2.wins -= 1
            team2.points -= 3
            team1.loses -= 1
        else:
            team1.draws -= 1
            team2.draws -= 1
            team1.points -= 1
            team2.points -= 1
    else:
        team1.goals_scored += match.goals_1
        team1.goals_lost += match.goals_2
        team2.goals_scored += match.goals_2
        team2.goals_lost += match.goals_1
        team1.matches_played += 1
        team2.matches_played += 1
        # Sprawdź, czy wartości są w odpowiednim zakresie
        if team1.matches_played > 3:
            team1.matches_played = 3
        if team2.matches_played > 3:
            team2.matches_played = 3
        if match.goals_1 > match.goals_2:
            team1.points += 3
            team1.wins += 1
            team2.loses += 1
        elif match.goals_1 < match.goals_2:
            team2.points += 3
            team2.wins += 1
            team1.loses += 1
        else:
            team1.draws += 1
            team1.points += 1
            team2.draws += 1
            team2.points += 1

    team1.save()
    team2.save()
    match.previous_goals_1 = match.goals_1
    match.previous_goals_2 = match.goals_2


@receiver(pre_save, sender=Match)
def handle_pre_save(sender, instance, **kwargs):
    if instance.pk:  # This is an update operation
        previous_instance = Match.objects.get(pk=instance.pk)
        instance.previous_goals_1 = previous_instance.goals_1
        instance.previous_goals_2 = previous_instance.goals_2
        update_teams(previous_instance, reset=True)

@receiver(post_save, sender=Match)
def handle_post_save(sender, instance, created, **kwargs):
    update_teams(instance)

class Group(models.Model):
    group_name = models.CharField(max_length=1)
    teams = models.ManyToManyField(Team)
    matches = models.ManyToManyField(Match, blank=True)

    def __str__(self):
        return self.group_name

    def clean(self):
        if self.pk and self.teams.count() > 4:
            raise ValidationError('Group can only have 4 teams')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        if self.pk:  # Ensure the group is saved before creating matches
            create_matches(self)
