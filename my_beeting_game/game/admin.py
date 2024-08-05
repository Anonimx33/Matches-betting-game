from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect, render
from .models import Team, Match, Group, create_matches
from .forms import GroupNameForm
import logging
logger = logging.getLogger(__name__)

class GroupAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Jeśli jest to nowy obiekt, a nie edytowany
            create_matches(obj)
            obj.save()  # Save again to ensure matches are created

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'matches_played', 'wins', 'draws', 'loses', 'goals_scored', 'goals_lost', 'points')
    search_fields = ('team_name',)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_date', 'goals_1', 'goals_2', 'get_teams')
    list_filter = ('match_date',)
    filter_horizontal = ('teams',)

    def get_teams(self, obj):
        return ", ".join([team.team_name for team in obj.teams.all()])
    get_teams.short_description = 'Teams'

admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Group, GroupAdmin)
