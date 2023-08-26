from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Avg
from django.utils.text import slugify

from urllib.parse import quote

User = get_user_model()

# Create your models here.
'''Choices options'''
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
COMMENTS_RAITING = (
    ('like', 'like'),
    ('heart', 'heart'),
    ('surprise', 'surprise'),
    ('laugh', 'laugh'),
)

'''UserGameEntry'''
class UserGameEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    games = models.ForeignKey('GameList', on_delete=models.PROTECT)
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

'''Game List'''
class GameList(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    video = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to='game/cover/', null=True, blank=True)
    game_type = models.ManyToManyField('Type')
    category = models.ManyToManyField('Category')
    developer = models.ForeignKey('GameDeveloper', on_delete=models.PROTECT)
    platforms = models.ManyToManyField('Platform', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    release_date = models.DateField(blank=True, null=True)
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
    
'''Category'''
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

'''Type'''
class Type(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
'''Games Developers'''
class GameDeveloper(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logo/')
    description = models.TextField(blank=True, null=True)
    founders = models.ManyToManyField('Founder', blank=True)
    established_date = models.DateField()
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}')
        super().save(*args, **kwargs)
    
'''Founder'''
def get_default_founder_avatar():
    return 'default/avatar/founder.jpg'

class Founder(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='founder_photos/', default=get_default_founder_avatar)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name}-{self.last_name}')
        super().save(*args, **kwargs)

'''Comments'''
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(GameList, on_delete=models.PROTECT)
    text = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.game.title}'
    
class CommentRaiting(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    comment_raiting = models.CharField(max_length=10, choices=COMMENTS_RAITING)
    
    def __str__(self):
        return f'{self.get_comment_raiting_display()} by {self.user.username}, on {self.comment}'
    
    class Meta:
        unique_together = ('user', 'comment', 'comment_raiting')

'''Tags'''
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

'''Platforms'''
class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
