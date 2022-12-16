# Generated by Django 3.2.4 on 2022-02-10 19:09

from django.conf import settings
from django.db import migrations, models
import pumpwood_communication.serializers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DescriptionExperimentTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=154, null=True)),
                ('notes', models.TextField(blank=True, default='')),
                ('dimentions', models.JSONField(blank=True, default=dict, encoder=pumpwood_communication.serializers.PumpWoodJSONEncoder)),
                ('user_set', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'experiment__team',
            },
        ),
    ]