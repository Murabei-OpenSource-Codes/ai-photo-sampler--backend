# Generated by Django 3.2.4 on 2022-04-11 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0006_auto_20220211_1359'),
    ]

    operations = [
        migrations.RenameField(
            model_name='descriptionexperimentteam',
            old_name='dimension',
            new_name='dimentions',
        ),
    ]