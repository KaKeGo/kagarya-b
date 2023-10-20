from django.contrib import admin

from .models import (
    BooksList, Rating, Category, Type
)

# Register your models here.


admin.site.register([BooksList, Rating, Category, Type])
