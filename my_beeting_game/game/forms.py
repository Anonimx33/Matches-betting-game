from django import forms
from .models import Team, Group

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

class GroupNameForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']
    