from django.db import models

# Create your models here.

ACCESS_CHOICES = [
    ('admin', 'Admin'),
    ('authenticated', 'Authenticated User'),
    ('any', 'Any')
]


class ApiUrls(models.Model):
    name = models.CharField(max_length=100)
    access = models.CharField(max_length=20, choices=ACCESS_CHOICES, default='admin')
    url = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    def url_count(self):
        return ApiUrls.objects.count()

class ApiCategory(models.Model):
    name = models.CharField(max_length=100)
    api = models.ManyToManyField('ApiUrls', blank=True)
    
    def __str__(self):
        return self.name
