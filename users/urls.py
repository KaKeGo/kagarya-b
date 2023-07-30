from django.urls import path

from . views import (
    GetCSRFToken,
    UserAuthCheckView,
    
    UserProfileDetailView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    
    ProfileListView,

)


app_name = 'users'


urlpatterns = [
    path('csrftoken/', GetCSRFToken.as_view(), name='csrftoken'),
    path('authcheck/', UserAuthCheckView.as_view(), name='user_auth_check'),
    
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/create/', UserRegisterView.as_view(), name='profile_create'),
    path('profile/login/', UserLoginView.as_view(), name='profile_login'),
    path('profile/logout/', UserLogoutView.as_view(), name='profile_logout'),
    
    path('profile/<slug>/', UserProfileDetailView.as_view(), name='profile_detail'),
]
