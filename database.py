from my_beeting_game.game.models import Team, Group

groupA = Group.objects.create(group_name='A')
groupB = Group.objects.create(group_name='B')

belgium = Team.objects.create(team_name='Belgium')
france = Team.objects.create(team_name='France')
poland = Team.objects.create(team_name='Poland')
albania = Team.objects.create(team_name='Albania') 

slovakia = Team.objects.create(team_name='Slovakia')
finland = Team.objects.create(team_name='Finland')
spain = Team.objects.create(team_name='Spain')
germany = Team.objects.create(team_name='Germany')

ga = [belgium, france, poland, albania]
gb = [slovakia, finland, spain, germany]

for team in ga:
    groupA.teams.add(team)
    
for team in gb:
    groupB.teams.add(team) 