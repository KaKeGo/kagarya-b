from django.urls import path

from .views import (
    GamesListView, AddGameToProfileView, PlatformCreatorListView, PlatformCreatorCreateView,
    PlatformCreateView, PlatformListView, TagListView, TagCreateView, TagUpdateView,
    CommentListView, CommentCreateView, CommentRatingCreateView, TypeListView, 
    TypeCreateView
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
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/create/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:tag_id>/update/', TagUpdateView.as_view(), name='tag_update'),
    # Comments
    path('comment/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:game_id>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:comment_id>/add/', CommentRatingCreateView.as_view(), name='comment_rating_create'),
    # Type
    path('type/', TypeListView.as_view(), name='type_list'),
    path('type/create/', TypeCreateView.as_view(), name='type_create'),
]
