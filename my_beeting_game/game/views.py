from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Team, Group, Match
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

def game(request):
    groups = Group.objects.all().values()
    template = loader.get_template('all_teams.html')
    context = {
        'groups': groups
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    group = Group.objects.get(id=id)
    teams = group.teams.all().order_by('-points', '-wins', '-goals_scored', 'team_name')
    if group.matches.count() != 6:
        group.matches.clear()
        for j in range(3):
            for i in range(2):
                if j == 0:
                    match = Match.objects.create()
                    match.teams.set([teams[2*i], teams[2*i+1]])
                if j == 1:
                    match = Match.objects.create()
                    match.teams.set([teams[i], teams[i+2]])
                if j == 2:
                    match = Match.objects.create()
                    match.teams.set([teams[i], teams[3-i]])
                group.matches.add(match)
    matches = group.matches.all().order_by('match_date')
    template = loader.get_template('group_details.html')
    context = {
        'group': group,
        'teams': teams,
        'matches': matches
    }
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('')
    else:
        form = UserCreationForm()
    return render(request, '/registration/register.html', {'form': form})


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())