from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('public', 'public'),
)


class AnimeList(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    anime_type = models.ManyToManyField('Type')
    episodes = models.IntegerField(default=0)
    category = models.ManyToManyField('Category')
    status= models.CharField(max_length=100, choices=STATUS_CHOICES)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def average_raiting(self):
        pass

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    anime = models.ForeignKey(AnimeList, related_name='ratings', on_delete=models.CASCADE)
    value = models.PositiveIntegerField(
            validators=[MinValueValidator(1), MaxValueValidator(10)]
        )
    
    def __str__(self):
        return f'{self.user.username} - {self.value}'
    
    class Meta:
        unique_together = ['anime', 'user']
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Type(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    