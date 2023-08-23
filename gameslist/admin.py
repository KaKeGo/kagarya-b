from django.contrib import admin

from .models import (
    GameList, Type, Category, UserGameEntry
)
# Register your models here.


admin.site.register([GameList, Type, Category, UserGameEntry])
