import random
import string

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

# Create your models here.


class TodoPlan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    todo = models.ManyToManyField('Todo', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def get_username(self):
        return self.author.username
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_name = f'{self.name}-{self.author.username}'
            self.slug = slugify(slug_name)
            super().save(*args, **kwargs)
    
class Todo(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.ManyToManyField('TodoCategory', blank=True)
    task = models.ManyToManyField('Task', blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    class Meta:
        ordering = ['date_created']
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def count_todo():
        return Todo.objects.count()
    
    def random_slug(self, length):
        r_slug = string.ascii_letters + string.digits
        return ''.join(random.choice(r_slug) for _ in range(length))
    
    def save(self, *args, **kwargs):
        if not self.slug:
            r_slug = self.random_slug(10)
            self.slug = slugify(self.name + '-' + r_slug)
        super().save(*args, **kwargs)
    
class Task(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def count_tasks():
        return Task.objects.count()
    
class TodoCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name
    
