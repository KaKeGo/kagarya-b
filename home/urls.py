from django.urls import path

from .views import (
    homeView, send_email,
)

app_name = 'home'


urlpatterns = [
    path('', homeView, name='home'),
    path('send_email/', send_email, name='send_email'),
]

