from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from .models import Roles
from .profile_model import (
    Profile, Gender,
)


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''Create profile when user create'''
    if created:
        Profile.objects.create(
                user=instance
            )

@receiver(post_save, sender=User)
def create_gender(sender, instance, **kwargs):
    '''Create gender when user is created'''
    if not Gender.objects.exists():
        genders = ['Male', 'Female']
        for gender_name in genders:
            Gender.objects.create(
                name=gender_name
            )

@receiver(pre_save, sender=Profile)
def slug_save(sender, instance, **kwargs):
    if not instance.slug:
        username = instance.user.username
        user_id = instance.user.id
        slug = f'{slugify(username)}i{user_id}'
        
        counter = 1
        while Profile.objects.filter(slug=slug).exists():
            slug = f'{slug}i{counter}'
            counter += 1
        
        instance.slug = slug

@receiver(post_save, sender=User)
def create_roles(sender, instance, created, **kwargs):
    if created:
        roles = ['Admin', 'Staff', 'GameCreator']
        for role_name in roles:
            Roles.objects.get_or_create(
                title=role_name
            )
