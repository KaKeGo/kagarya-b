from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Avg

from urllib.parse import quote

User = get_user_model()


# Create your models here.

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('public', 'public'),
)
RAITING_CHOICE = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
)
PROGRESS_CHOICE = (
    ('playing', 'playing'),
    ('completed', 'completed'),
    ('on hold', 'on hold'),
    ('dropped', 'dropped'),
    ('plan to play', 'plan to play'),
)

class UserGameEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    games = models.ForeignKey('GameList', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, choices=PROGRESS_CHOICE, default='plan to play')
    rating = models.PositiveIntegerField(choices=RAITING_CHOICE)
    note = models.TextField(max_length=200, blank=True, null=True)
    added_date = models.DateField(default=timezone.now, blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} / game / {self.games.title}'
    
    def set_rating(self, value):
        if self.rating:
            self.rating.value = value
            self.rating.save()
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.finish_date:
            self.finish_date = timezone.now().date()
        
        super().save(*args, **kwargs)
        self.user.profile.game_list.add(self)

class GameList(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    video = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to='game/cover/', null=True, blank=True)
    game_type = models.ManyToManyField('Type')
    category = models.ManyToManyField('Category')
    status= models.CharField(max_length=100, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)
        if not self.slug:
            self.slug = quote(f'{self.id}/{self.title}')
        super().save(*args, **kwargs)
    
    @property
    def average_rating(self):
        avg_rating = UserGameEntry.objects.filter(games=self).aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 2)
        return 0

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    