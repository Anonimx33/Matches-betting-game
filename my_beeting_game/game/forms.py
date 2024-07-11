from django import forms
from .models import Team, Group, Membership

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']