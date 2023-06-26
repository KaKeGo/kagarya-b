from django.db import models

# Create your models here.


class TodoPlan(models.Model):
    name = models.CharField(max_length=30)
    todo = models.ManyToManyField('Todo', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Todo(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    category = models.ManyToManyField('Category', blank=True, null=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def count_todo(self):
        return Todo.objects.count()
    
class Task(models.Model):
    name = models.CharField(max_length=40)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def count_tasks(self):
        return Task.objects.count()
    
