from django.urls import path

from .consumers import MyWebSocketConsumer


websocket_urlpatterns = [
    path('sock/account/authcheck/', MyWebSocketConsumer.as_asgi()),
]
