from django.urls import path

from .views import (
    GamesListView,
)

app_name = 'gamelist'


urlpatterns = [
    path('', GamesListView.as_view(), name='list'),
]

