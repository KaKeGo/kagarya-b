# Generated by Django 4.2.2 on 2023-10-20 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filmslist', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='raiting',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='film_ratings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='filmslist',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='filmslist',
            name='category',
            field=models.ManyToManyField(to='filmslist.category'),
        ),
        migrations.AddField(
            model_name='filmslist',
            name='film_type',
            field=models.ManyToManyField(to='filmslist.type'),
        ),
        migrations.AlterUniqueTogether(
            name='raiting',
            unique_together={('film', 'user')},
        ),
    ]
