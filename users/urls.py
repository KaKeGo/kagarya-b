from django.urls import path

from . views import (
    ProfileListView,
)


app_name = 'users'


urlpatterns = [
    path('profilelist/', ProfileListView.as_view(), name='profile_list'),
]

