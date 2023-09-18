from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.db.models import Avg, F, FloatField
from django.db.models.functions import Coalesce

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    GameList, Type, Category, PlatformCreator, Platform, Tag, Comment, CommentRaiting,
)
from .serializers import (
    GamesListSerializer, GameListCreateSerializer, GameUpdateSerializer,
    UserGameEntrySerializer, 
    PlatformCreatorSerializer, PlatformCreatorCreateSerializer, PlatformCreatorUpdateSerializer,
    PlatformListSerializer,PlatformCreateSerializer, PlatformUpdateSerializer,
    TagListSerializer, TagCreateSerializer, TagUpdateSerializer,
    CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer,
    CommentRatingCreateSerializer, CommentRaitingUpdateSerializer,
    TypeSerializer, TypeCreateSerializer, TypeUpdateSerializer, 
    CategoryCreateSerializer, CategorySerializer, CategoryUpdateSerializer,
)


'''Game List'''
class GamesListView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def get(self, request):
        game_list = GameList.objects.all()
        serializer = GamesListSerializer(game_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GameListDetailView(APIView):
    def get(self, request, slug):
        game_list = get_object_or_404(GameList, slug=slug)
        serializer = GamesListSerializer(game_list)
        return Response(serializer.data, status=status.HTTP_200_OK)

@method_decorator(csrf_protect, name='dispatch')
class GameListCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = GameListCreateSerializer(data=request.data)
        if serializer.is_valid():
            game_list = serializer.save()
            
            game_list.slug = slugify(f'{game_list.id}/{game_list.title}')
            game_list.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class GameListUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, slug):
        try:
            game = GameList.objects.get(slug=slug)
        except GameList.DoesNotExist:
            return Response({'message': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = GameUpdateSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class GameListDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, slug):
        try:
            game_list = GameList.objects.get(slug=slug)
        except GameList.DoesNotExist:
            return Response({'message': 'Game not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        game_list.delete()
        return Response({'message': 'Game deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

'''Games event list'''
class RecentlyAddedGamesView(APIView):
    def get(self, request):
        games = GameList.objects.order_by('-id')[:5]
        serializer = GamesListSerializer(games, many=True)
        return Response(serializer.data)

class TopRatedGamesView(APIView):
    def get(self, request):
        top_rated_games = GameList.objects.annotate(
            avg_rating=Coalesce(Avg(F('usergameentry__rating')), 0, output_field=FloatField())
        ).order_by('-avg_rating')[:10]

        serializer = GamesListSerializer(top_rated_games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''Game List Entry'''
@method_decorator(csrf_protect, name='dispatch')
class AddGameToProfileView(APIView):
    def post(self, request):
        serializer = UserGameEntrySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''Platform Creator'''
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
        serializer = PlatformCreatorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class PlatformCreatorUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def put(self, request, pk):
        try:
            platform_creator = PlatformCreator.objects.get(pk=pk)
        except PlatformCreator.DoesNotExist:
            return Response({'message': 'Platform creator not found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PlatformCreatorUpdateSerializer(platform_creator, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class PlatformCreatorDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, pk):
        try:
            platform_creator = PlatformCreator.objects.get(pk=pk)
        except PlatformCreator.DoesNotExist:
            return Response({'message': 'Platgorm creator not found'}, status=status.HTTP_404_NOT_FOUND)
        
        platform_creator.delete()
        return Response({'message': 'Platform creator deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

'''Platform'''
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

@method_decorator(csrf_protect, name='dispatch')
class PlatformUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, pk):
        try:
            platform_instance = Platform.objects.get(pk=pk)
        except Platform.DoesNotExist:
            return Response({'message': 'Platform not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PlatformUpdateSerializer(platform_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class PlatformDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, pk):
        try:
            platform = Platform.objects.get(pk=pk)
        except Platform.DoesNotExist:
            return Response({'message': 'Platform not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        platform.datele()
        return Response({'message': 'Platform deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

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
    
    def put(self, request, pk):
        try:
            tag_instance = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({'message': 'Tag not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TagUpdateSerializer(tag_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class TagDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, pk):
        try:
            tag_instance = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response({'message': 'Tag not found.'}, status=status.HTTP_404_NOT_FOUND)

        tag_instance.delete()
        return Response({'message': 'Tag deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

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
    
    def post(self, request, pk):
        game = GameList.objects.get(pk=pk)
        serializer = CommentCreateSerializer(data=request.data, context={
            'game': game, 'request': request
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CommentUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentUpdateSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CommentDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        comment.delete()
        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

'''Comment Raiting'''
@method_decorator(csrf_protect, name='dispatch')
class CommentRatingCreateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def post(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentRatingCreateSerializer(data=request.data, context={
                'request': request, 'comment': comment
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CommentRaitingUpdateView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def put(self, request, pk):
        try:
            comment_raiting = CommentRaiting.objects.get(pk=pk)
        except CommentRaiting.DoesNotExist:
            return Response({'message': 'Comment Raiting not found'}, status=status.HTTP_204_NO_CONTENT)

        serializer = CommentRaitingUpdateSerializer(comment_raiting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CommentRaitingDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, pk):
        try:
            comment_raiting = CommentRaiting.objects.get(pk=pk)
        except CommentRaiting.DoesNotExist:
            return Response({'message': 'Comment raiting not found'}, status=status.HTTP_404_NOT_FOUND)
        
        comment_raiting.delete()
        return Response({'message': 'Comment raiting deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        

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
    
    def put(self, request, pk):
        try:
            type_instance = Type.objects.get(pk=pk)
        except Type.DoesNotExist:
            return Response({'message': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TypeUpdateSerializer(type_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class TypeDeleteView(APIView):
    permission_classes = [permissions.AllowAny, ]
    
    def delete(self, request, pk):
        try:
            type_instance = Type.objects.get(pk=pk)
        except Type.DoesNotExist:
            return Response({'message': 'Type not found'}, status=status.HTTP_404_NOT_FOUND)
        
        type_instance.delete()
        return Response({'message': 'Type deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

'''Category'''
class CategoryListView(APIView):
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
    
    def put(self, request, pk):
        try:
            category_instance = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryUpdateSerializer(category_instance, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class CategoryDeleteView(APIView):
    def delete(self, request, pk):
        try:
            category_instance = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        category_instance.delete()
        return Response({'message': 'Category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)        
