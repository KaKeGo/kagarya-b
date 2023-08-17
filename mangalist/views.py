from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    MangaList, Category, Type
)
from .serializers import (
    MangaListSerializer,
    
    TypeSerializer,
    
    CategorySerializer,
)


class MangaListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        manga_list = MangaList.objects.all()
        serializer = MangaListSerializer(manga_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
