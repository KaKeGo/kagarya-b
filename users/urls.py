from django.urls import path

from . views import (
    GetCSRFToken,
    
    UserProfileDetailView,
    UserRegisterView,
    
    ProfileListView,

)


app_name = 'users'


urlpatterns = [
    path('csrftoken/', GetCSRFToken.as_view(), name='csrftoken'),
    path('profilelist/', ProfileListView.as_view(), name='profile_list'),
    path('profile/create/', UserRegisterView.as_view(), name='profile_create'),
    
    path('profile/<slug:slug>/', UserProfileDetailView.as_view(), name='profile_detail'),
]

