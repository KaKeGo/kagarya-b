import random, string

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Avg, Count
from django.utils.text import slugify

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
    ('trash', 'trash'),
)
GAME_VERSION = (
    ('alpha', 'alpha'),
    ('beta', 'beta'),
    ('early access', 'early access'),
    ('full release', 'full release'),
)
GAME_MODE = (
    ('single-player', 'single-player'),
    ('online PvP', 'online PvP'),
    ('online co-op', 'online co-op'),
    ('cross-platform multiplayer', 'cross-platform multiplayer'),
)

def generate_random_slug(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_default_game_avatar():
    '''Default avatar for Game'''
    return 'default/game/default/defaultgame.jpg'

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
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    game_version = models.CharField(max_length=30, choices=GAME_VERSION, null=True, blank=True)
    game_mode = models.CharField(max_length=30, choices=GAME_MODE, null=True, blank=True)
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField(blank=True, null=True)
    trailer = models.URLField(blank=True, null=True)
    cover = models.ImageField(upload_to='game/cover/', default=get_default_game_avatar, null=True, blank=True)
    game_type = models.ManyToManyField('Type', blank=True)
    category = models.ManyToManyField('Category', blank=True)
    developer = models.ForeignKey('GameDeveloper', on_delete=models.PROTECT, blank=True, null=True, related_name='game_developer')
    game_publisher = models.ForeignKey('GamePublisher', on_delete=models.PROTECT, null=True, blank=True, related_name='game_publisher')
    platforms = models.ManyToManyField('Platform', blank=True)
    comments = models.ManyToManyField('Comment', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    release_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    game_slug = models.SlugField(unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        avg_rating = UserGameEntry.objects.filter(games=self).aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 2)
        return 0
    
    class Meta:
        ordering = ['-release_date']
    
'''Category'''
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

'''Type'''
class Type(models.Model):
    name = models.CharField(max_length=100,  null=True, unique=True)
    
    def __str__(self):
        return self.name

'''Game Developers'''
class GameDeveloper(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='company_logo/')
    description = models.TextField(blank=True, null=True)
    founders = models.ManyToManyField('Founder', blank=True)
    established_date = models.DateField()
    developer_slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}')
        super().save(*args, **kwargs)
        
def get_default_founder_avatar():
    return 'default/avatar/founder.jpg'

'''Game Publisher'''
class GamePublisher(GameDeveloper):
    pass

'''Founder'''
class Founder(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='founder_photos/', default=get_default_founder_avatar)
    founder_slug = models.SlugField(unique=True, blank=True)
    
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
    
    def count_ratings(self):
        ratings = self.commentraiting_set.values('comment_rating').annotate(total=Count('comment_rating'))
        raiting_counts = {rating['comment_rating']: rating['total'] for rating in ratings}
        return raiting_counts
    
    @property
    def formatted_created_at(self):
        return self.created_at.strftime('%d-%m-%Y %H:%M')
    
class CommentRaiting(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    comment_rating = models.CharField(max_length=10, choices=COMMENTS_RAITING)
    
    def __str__(self):
        return f'{self.get_comment_rating_display()} by {self.user.username}, on {self.comment}'
    
    class Meta:
        unique_together = ('user', 'comment', 'comment_rating')

'''Tags'''
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

'''Platforms'''
class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='platform_photos/', default=get_default_founder_avatar)
    description = models.TextField(max_length=500, blank=True, null=True)
    date_established = models.DateField(blank=True, null=True)
    creator = models.ManyToManyField('PlatformCreator', blank=True)
    platform_slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            random_slug = generate_random_slug()
            self.slug = slugify(f'{self.name}-{random_slug}')
        super().save(*args, **kwargs)

class PlatformCreator(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    bio = models.TextField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to='founder_photos/', default=get_default_founder_avatar)
    platform_creator_slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.first_name}-{self.last_name}')
        super().save(*args, **kwargs)
