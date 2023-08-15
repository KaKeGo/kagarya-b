from django.contrib import admin

from .models import (
    AnimeList, Rating, Category, Type
)

# Register your models here.


admin.site.register([AnimeList, Rating, Category, Type])
