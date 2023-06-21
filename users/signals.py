from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile, Gender


User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''Create profile when user create'''
    if created:
        Profile.objects.create(
                user=instance
            )

@receiver(pre_save, sender=User)
def check_gender_exists(sender, instance, **kwargs):
    if not Gender.objects.exists():
        genders = ['Male', 'Female']
        for gender_name in genders:
            Gender.objects.create(
                name=gender_name
            )
