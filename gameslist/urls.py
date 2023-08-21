from django.urls import path

from .views import (
    GamesListView,
    AddGameToProfileView,
)

app_name = 'gamelist'


urlpatterns = [
    path('', GamesListView.as_view(), name='list'),
    path('add-game/', AddGameToProfileView.as_view(), name='add_game'),
]
