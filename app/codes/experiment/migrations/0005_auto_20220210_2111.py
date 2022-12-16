# Generated by Django 3.2.4 on 2022-02-10 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('experiment', '0004_auto_20220210_2045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descriptionexperimentteam',
            name='user_set',
        ),
        migrations.AlterField(
            model_name='experimentteamuser',
            name='user',
            field=models.OneToOneField(help_text='User associated to team', on_delete=django.db.models.deletion.CASCADE, related_name='experiment_team', to=settings.AUTH_USER_MODEL, verbose_name='User associated to team'),
        ),
    ]