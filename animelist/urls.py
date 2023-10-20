from django.urls import path

from .views import (
    AnimeListView,
)

app_name = 'animelist'


urlpatterns = [
    path('', AnimeListView.as_view(), name='list'),
]

