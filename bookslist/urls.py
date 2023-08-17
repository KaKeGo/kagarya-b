from django.urls import path

from .views import (
    BooksListView,
)

app_name = 'animelist'


urlpatterns = [
    path('', BooksListView.as_view(), name='list'),
]

