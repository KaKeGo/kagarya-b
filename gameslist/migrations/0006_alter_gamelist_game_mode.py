# Generated by Django 4.2.2 on 2023-11-26 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameslist', '0005_alter_gamelist_game_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamelist',
            name='game_mode',
            field=models.ManyToManyField(blank=True, to='gameslist.gamemode'),
        ),
    ]