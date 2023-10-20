from django.urls import path

from .views import (
    MangaListView,
)

app_name = 'mangalist'


urlpatterns = [
    path('', MangaListView.as_view(), name='list'),
]

