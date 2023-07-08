# Generated by Django 4.2.2 on 2023-07-08 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('todo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='todoplan',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='todoplan',
            name='todo',
            field=models.ManyToManyField(blank=True, null=True, to='todo.todo'),
        ),
        migrations.AddField(
            model_name='todo',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='todo.todocategory'),
        ),
        migrations.AddField(
            model_name='todo',
            name='task',
            field=models.ManyToManyField(blank=True, null=True, to='todo.task'),
        ),
    ]
