from django.contrib import admin

from .models import (
    MangaList, Raiting, Type, Category
)

# Register your models here.


admin.site.register([MangaList, Raiting, Type, Category])
