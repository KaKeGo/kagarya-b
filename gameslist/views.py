from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    GameList,
    Type,
    Category,
)
from .serializers import (
    GamesListSerializer,
)


class GamesListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        game_list = GameList.objects.all()
        serializer = GamesListSerializer(game_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
