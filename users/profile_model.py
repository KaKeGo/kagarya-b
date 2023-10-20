from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model

from gameslist.models import UserGameEntry

User = get_user_model()


# from gameslist.models import UserGameList

# Create your models here.


'''
Profile for users
'''

def get_default_avatar():
    '''Default avatar for users'''
    return 'default/avatar/avatar.jpg'

class Gender(models.Model):
    name = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default=get_default_avatar)
    about = models.TextField(blank=True, null=True)
    motto = models.CharField(max_length=80, blank=True, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    
    game_list = models.ManyToManyField(UserGameEntry, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

    def get_username(self):
        return self.user.username
    
    @property
    def total_games_added(self):
        return self.game_list.count()
    
    @property
    def games_by_status_count(self):
        status_mapping = {
            'completed': 'completed_games',
            'playing': 'playing_games',
            'on hold': 'on_hold_games',
            'dropped': 'dropped_games',
            'plan to play': 'plan_to_play_games',
        }
        
        games_count_by_status = {}
        for status_code, status_display in status_mapping.items():
            filter_kwargs = {'status': status_code}
            count = self.game_list.filter(**filter_kwargs).count()
            games_count_by_status[status_display] = count
        
        return games_count_by_status
    
    @property
    def recently_added_games(self):
        return self.game_list.order_by('-added_date')[:5]
