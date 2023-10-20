from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    BooksList, Category, Type
)
from .serializers import (
    BooksListSerializer,
    
    TypeSerializer,
    
    CategorySerializer,
)


class BooksListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        books_list = BooksList.objects.all()
        serializer = BooksListSerializer(books_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
