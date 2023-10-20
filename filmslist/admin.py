from django.contrib import admin

from .models import (
    FilmsList, Category, Type, Raiting
)

# Register your models here.


admin.site.register([FilmsList, Category, Type, Raiting])
