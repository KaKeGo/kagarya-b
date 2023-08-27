from django.urls import path

from .views import (
    GamesListView, AddGameToProfileView, PlatformCreatorListView, PlatformCreatorCreateView,
    PlatformCreateView, PlatformListView,
)

app_name = 'gamelist'


urlpatterns = [
    # GameList
    path('', GamesListView.as_view(), name='game_list'),
    path('add-game/', AddGameToProfileView.as_view(), name='add_game_to_list'),
    # Platfroms
    path('platform/', PlatformListView.as_view(), name='platform_list'),
    path('platform/create/', PlatformCreateView.as_view(), name='platform_create'),
    path('platform/creators/', PlatformCreatorListView.as_view(), name='platform_creators_list'),
    path('platform/creators/create/', PlatformCreatorCreateView.as_view(), name='platform_creator_create'),
]
