from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class TodoPlan(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    todo = models.ManyToManyField('Todo', blank=True, null=True)
    
    def get_username(self):
        return self.author.username
    
    def __str__(self):
        return self.name
    
class Todo(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.ManyToManyField('TodoCategory', blank=True, null=True)
    task = models.ManyToManyField('Task', blank=True, null=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def count_todo():
        return Todo.objects.count()
    
class Task(models.Model):
    name = models.CharField(max_length=40)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def count_tasks():
        return Task.objects.count()
    
class TodoCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name
    
