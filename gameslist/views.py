from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    GameList, Type, Category, PlatformCreator, Platform,
)
from .serializers import (
    GamesListSerializer, UserGameEntrySerializer, PlatformCreatorSerializer, PlatformSerializer,
    
)

'''Game List'''
class GamesListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        game_list = GameList.objects.all()
        serializer = GamesListSerializer(game_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''Game List Entry'''
class AddGameToProfileView(APIView):
    def post(self, request):
        serializer = UserGameEntrySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Platform'''
class PlatformCreatorListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        creators = PlatformCreator.objects.all()
        serializer = PlatformCreatorSerializer(creators, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class PlatformCreatorCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = PlatformCreatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlatformListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        platforms = Platform.objects.all()
        serializer = PlatformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class PlatformCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = PlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
