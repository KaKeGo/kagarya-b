from django.urls import path

from .views import (
    GamesListView, GameListDetailView, GameListCreateView, GameListUpdateView, GameListDeleteView,
    AddGameToProfileView, 
    PlatformCreatorListView, PlatformCreatorCreateView, PlatformCreatorUpdateView, PlatformCreatorDeleteView,
    PlatformCreateView, PlatformListView, PlatformUpdateView, PlatformDeleteView,
    TagListView, TagCreateView, TagUpdateView, TagDeleteView,
    CommentListView, CommentCreateView, CommentUpdateView, CommentDeleteView,
    CommentRatingCreateView, CommentRaitingUpdateView, CommentRaitingDeleteView,
    TypeListView, TypeCreateView, TypeUpdateView,TypeDeleteView,
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    RecentlyAddedGamesView, TopRatedGamesView, UpcomingGameListView, RelesedTodayGameView,
    RecentlyReleasedGameView,
    GameDeveloperListView, GameDeveloperCreateView,
)

app_name = 'gamelist'


urlpatterns = [
    # GameList
    path('list/<str:game_status>/', GamesListView.as_view(), name='game_list_by_status'),
    path('create/', GameListCreateView.as_view(), name='game_create'),
    path('detail/<slug>/', GameListDetailView.as_view(), name='game_detail'),
    path('<slug>/update/', GameListUpdateView.as_view(), name='game_update'),
    path('<slug>/delete/', GameListDeleteView.as_view(), name='game_delete'),
    # User Add Game List
    path('add-game/', AddGameToProfileView.as_view(), name='add_game_to_list'),
    # Platfroms
    path('platform/', PlatformListView.as_view(), name='platform_list'),
    path('platform/create/', PlatformCreateView.as_view(), name='platform_create'),
    path('platform/<int:pk>/update/', PlatformUpdateView.as_view(), name='platform_update'),
    path('platform/<int:pk>/delete/', PlatformDeleteView.as_view(), name='platform_delete'),
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
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    # Comments Raiting
    path('comment/raiting/<int:pk>/add/', CommentRatingCreateView.as_view(), name='comment_rating_create'),
    path('comment/raiting/<int:pk>/update/', CommentRaitingUpdateView.as_view(), name='comment_rating_create'),
    path('comment/raiting/<int:pk>/delete/', CommentRaitingDeleteView.as_view(), name='comment_rating_create'),
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
    # Game developer
    path('developer/list/', GameDeveloperListView.as_view(), name='developer_list'),
    path('developer/create/', GameDeveloperCreateView.as_view(), name='developer_create'),
    #Games events
    path('recentlygames/', RecentlyAddedGamesView.as_view(), name='recentlygames'),
    path('topratedgames/', TopRatedGamesView.as_view(), name='topratedgames'),
    path('upcoming-games/', UpcomingGameListView.as_view(), name='upcoming_games'),
    path('today-relesed-games/', RelesedTodayGameView.as_view(), name='today_relesed_games'),
    path('recently-relesed-games/', RecentlyReleasedGameView.as_view(), name='recently_relesed_games'),
]
