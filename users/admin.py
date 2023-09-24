from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .profile_model import (
    Profile, Gender
)
from .models import User, Roles
from .forms import (
    UserCreateForm,
    UserUpdateForm,
)

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserUpdateForm
    model = User
    list_display = ('username', 'email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active',)}),
        ('Role', {'fields': ('roles',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
admin.site.register(User, CustomUserAdmin)
admin.site.register([Profile, Gender, Roles])
