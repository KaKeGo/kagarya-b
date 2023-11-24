# Generated by Django 4.2.2 on 2023-10-29 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gameslist.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gameslist', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamedeveloper',
            name='established_date',
            field=models.DateField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='gamedeveloper',
            name='logo',
            field=models.ImageField(default=gameslist.models.get_default_founder_avatar, upload_to='company_logo/'),
        ),
        migrations.CreateModel(
            name='GameReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reated_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameslist.gamelist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'game')},
            },
        ),
    ]