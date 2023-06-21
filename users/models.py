from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.sessions.models import Session
from django.utils import timezone

# Create your models here.

'''
CustomUser model and UserManager
'''

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set for user')
        if not username:
            raise ValueError('Username must be set for user')
        
        email = self.normalize_email(email)
        user = self.model(
                username=username, 
                email=email, 
                **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(
                username,
                email,
                password,
                **extra_fields
            )
        
    def count_created_users(self):
        return self.filter(superuser=False).count()

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now())
    last_login = models.DateTimeField(default=timezone.now())
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f'{self.username} | {self.email}'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def user_count(self):
        return User.objects.count_created_users()

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
    motto = models.CharField(max_length=80)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'

    def get_online_status(self):
        '''Show online status'''
        if self.user.last_login:
            session = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_key__in=self.user.session_set.value('session_key'),
            )
            return session.exists()
        return False
