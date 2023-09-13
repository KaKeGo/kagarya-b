from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    GameList, Type, Category, PlatformCreator, Platform, Tag, Comment, CommentRaiting,
)
from .serializers import (
    GamesListSerializer, UserGameEntrySerializer, PlatformCreatorSerializer, PlatformListSerializer,
    PlatformCreateSerializer, TagListSerializer, TagCreateSerializer, TagUpdateSerializer,
    CommentSerializer, CommentCreateSerializer, CommentRatingCreateSerializer, TypeCreateSerializer, TypeSerializer,
    TypeUpdateSerializer, CategoryCreateSerializer, CategorySerializer, CategoryUpdateSerializer,
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
        serializer = PlatformListSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class PlatformCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = PlatformCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Tag'''
class TagListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagListSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class TagCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = TagCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class TagUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, tag_id):
        try:
            tag_instance = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            return Response({'message': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TagUpdateSerializer(tag_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Comment'''
class CommentListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class CommentCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request, game_id):
        game = GameList.objects.get(pk=game_id)
        serializer = CommentCreateSerializer(data=request.data, context={
            'game': game, 'request': request
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CommentRatingCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentRatingCreateSerializer(data=request.data, context={
                'request': request, 'comment': comment
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Type'''
class TypeListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        type = Type.objects.all()
        serializer = TypeSerializer(type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class TypeCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, reqiest):
        serializer = TypeCreateSerializer(data=reqiest.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class TypeUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, type_id):
        try:
            type_instance = Type.objects.get(pk=type_id)
        except Type.DoesNotExist:
            return Response({'message': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TypeUpdateSerializer(type_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Category'''
class CategoryListSerializer(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class CategoryCreateView(APIView):
    permission_classes = [permissions.AllowAny, ] 
    
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CategoryUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, category_id):
        try:
            category_instance = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryUpdateSerializer(category_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CategoryDeleteView(APIView):
    def delete(self, request, category_id):
        try:
            category_instance = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        category_instance.delete()
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)        
