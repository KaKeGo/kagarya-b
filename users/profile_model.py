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
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    
    game_list = models.ManyToManyField(UserGameEntry, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

    def get_username(self):
        return self.user.username
