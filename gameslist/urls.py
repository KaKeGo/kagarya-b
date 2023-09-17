from django.urls import path

from .views import (
    GamesListView, AddGameToProfileView, 
    PlatformCreatorListView, PlatformCreatorCreateView, PlatformCreatorUpdateView, PlatformCreatorDeleteView,
    PlatformCreateView, PlatformListView, 
    TagListView, TagCreateView, TagUpdateView, TagDeleteView,
    CommentListView, CommentCreateView, 
    CommentRatingCreateView, 
    TypeListView, TypeCreateView, TypeUpdateView,TypeDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
)

app_name = 'gamelist'


urlpatterns = [
    # GameList
    path('', GamesListView.as_view(), name='game_list'),
    # User Add Game List
    path('add-game/', AddGameToProfileView.as_view(), name='add_game_to_list'),
    # Platfroms
    path('platform/', PlatformListView.as_view(), name='platform_list'),
    path('platform/create/', PlatformCreateView.as_view(), name='platform_create'),
    # Platgorm creators
    path('platform/creators/', PlatformCreatorListView.as_view(), name='platform_creators_list'),
    path('platform/creators/create/', PlatformCreatorCreateView.as_view(), name='platform_creator_create'), 
    path('platform/creators/<int:pk>/update/', PlatformCreatorUpdateView.as_view(), name='platform_creator_update'), 
    path('platform/creators/<int:pk>/delete/', PlatformCreatorDeleteView.as_view(), name='platform_creator_delete'), 
    # Tags
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('tags/create/', TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/update/', TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete/', TagDeleteView.as_view(), name='tag_delete'),
    # Comments
    path('comment/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/create/', CommentCreateView.as_view(), name='comment_create'),
    # Comments Raiting
    path('comment/<int:pk>/add/', CommentRatingCreateView.as_view(), name='comment_rating_create'),
    # Type
    path('type/', TypeListView.as_view(), name='type_list'),
    path('type/create/', TypeCreateView.as_view(), name='type_create'),
    path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type_update'),
    path('type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type_delete'),
    # Category
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]
