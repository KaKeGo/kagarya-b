from django.urls import path

from .views import (
    FilmsListView,
)

app_name = 'filmslist'


urlpatterns = [
    path('', FilmsListView.as_view(), name='list'),
]

