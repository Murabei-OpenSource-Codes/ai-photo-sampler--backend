# Generated by Django 3.2.4 on 2022-02-11 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiment', '0005_auto_20220210_2111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='descriptionexperimentteam',
            options={'verbose_name': 'Experiment Team', 'verbose_name_plural': 'Experiment Teams'},
        ),
        migrations.AlterModelOptions(
            name='experimentteamuser',
            options={'verbose_name': 'Team/User association', 'verbose_name_plural': 'Team/User associations'},
        ),
        migrations.RenameField(
            model_name='descriptionexperimentteam',
            old_name='dimentions',
            new_name='dimension',
        ),
        migrations.AlterField(
            model_name='descriptionexperimentteam',
            name='created_at',
            field=models.DateTimeField(blank=True, help_text='Date/Time team creation', verbose_name='Date/Time team creation'),
        ),
        migrations.AlterField(
            model_name='descriptionexperimentteam',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User that created team', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_experiment_team', to=settings.AUTH_USER_MODEL, verbose_name='User that created team'),
        ),
    ]