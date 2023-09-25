from django.urls import path

from . views import (
    GetCSRFToken, UserAuthCheckView, ActivateAccountView,
    UserProfileDetailView,
    UserRegisterView, UserLoginView, UserLogoutView,
    ProfileListView,
    RoleListView, RoleCreateView,
)


app_name = 'users'


urlpatterns = [
    path('csrftoken/', GetCSRFToken.as_view(), name='csrftoken'),
    path('authcheck/', UserAuthCheckView.as_view(), name='user_auth_check'),
    #Profile
    path('profile/list/', ProfileListView.as_view(), name='profile_list'),
    path('profile/create/', UserRegisterView.as_view(), name='profile_create'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate_account'),
    path('profile/login/', UserLoginView.as_view(), name='profile_login'),
    path('profile/logout/', UserLogoutView.as_view(), name='profile_logout'),
    #User Profile
    path('profile/<slug>/', UserProfileDetailView.as_view(), name='profile_detail'),
    #Roles
    path('roles/', RoleListView.as_view(), name='roles_list'),
    path('roles/create/', RoleCreateView.as_view(), name='roles_create'),
]
