from django.db import models
from django.contrib.auth import get_user_model

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
    ('plaing', 'plaing'),
    ('comleted', 'comleted'),
    ('on hold', 'on hold'),
    ('dropped', 'dropped'),
    ('plan to play', 'plan to play'),
)

class UserGameEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    games = models.ForeignKey('GameList', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, choices=PROGRESS_CHOICE, default='plan to play')
    
    def __str__(self):
        return f'{self.user.username} / game / {self.games.title}'
    
    def save(self, *args, **kwargs):
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
    def average_raiting(self):
        total_ratings = Rating.objects.filter(game=self).aggregate(models.Avg('value'))
        avg_rating = total_ratings['value__avg']
        if avg_rating is not None:
            return round(avg_rating, 2)
        return 0

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game = models.ForeignKey(GameList, related_name='ratings', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(choices=RAITING_CHOICE)
    
    def __str__(self):
        return f'{self.user.username} - {self.value}'
    
    class Meta:
        unique_together = ['game', 'user']
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    