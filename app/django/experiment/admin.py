from django.contrib import admin
from django import forms
from experiment.models import DescriptionExperimentTeam, ExperimentTeamUser
from flat_json_widget.widgets import FlatJsonWidget


class DescriptionExperimentTeamForm(forms.ModelForm):
    class Meta:
        widgets = {
            'dimensions': FlatJsonWidget
        }


@admin.register(DescriptionExperimentTeam)
class DescriptionExperimentTeamAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'description', 'notes', 'created_by', 'created_at'
    ]
    readonly_fields = [
        'created_by', 'created_at'
    ]
    form = DescriptionExperimentTeamForm

    fieldsets = [
        ['General Information', {
            'fields': (
                "description", "notes", 'created_by', 'created_at')}],
        ['Dimentions/Extra Info.', {
            'fields': (
                "dimensions",)}],
    ]


@admin.register(ExperimentTeamUser)
class ExperimentTeamUserAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'team'
    ]
    fields = [
        'user', 'team'
    ]
    readonly_fields = [
        'user'
    ]
