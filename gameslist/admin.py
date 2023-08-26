from django.contrib import admin

from .models import (
    GameList, Type, Category, UserGameEntry, Comment, CommentRaiting,
    GameDeveloper, Founder, Platform, Tag,
)
# Register your models here.


admin.site.register([
        GameList, Type, Category, UserGameEntry, Comment, CommentRaiting,
        GameDeveloper, Founder, Platform, Tag,
    ])
