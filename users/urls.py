from django.urls import path

from . views import (
    GetCSRFToken,
    
    UserProfileDetailView,
    UserRegisterView,
    UserLoginView,
    
    ProfileListView,

)


app_name = 'users'


urlpatterns = [
    path('csrftoken/', GetCSRFToken.as_view(), name='csrftoken'),
    
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/create/', UserRegisterView.as_view(), name='profile_create'),
    path('profile/login/', UserLoginView.as_view(), name='profile_login'),
    
    path('profile/<slug:slug>/', UserProfileDetailView.as_view(), name='profile_detail'),
]
