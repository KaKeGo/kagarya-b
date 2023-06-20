from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
)

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        })
    )
    

admin.site.register(User, CustomUserAdmin)
