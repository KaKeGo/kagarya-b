from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from PIL import Image


from .models import (
    GameList, Type, Category, UserGameEntry
)

User = get_user_model()


'''Anime Category'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

'''Anime Type'''
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']
        
'''Game Serializer'''
class GamesListSerializer(serializers.ModelSerializer):
    game_type = TypeSerializer(many=True)
    category = CategorySerializer(many=True)
    
    class Meta:
        model = GameList
        fields = [
                'id', 'cover', 'title', 'body', 'game_type',
                'category', 'average_raiting' 
            ]

class GameListCreateSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField()
    video = serializers.URLField(validators=[URLValidator()])
    
    class Meta:
        model = GameList
        fields = [
            'title', 'body', 'video', 'cover', 'game_type', 'category',
            'status'
        ]
        
    def validate_title(self, value):
        if len(value) <0:
            raise serializers.ValidationError('Title should be at least 2 characters')
        elif len(value) >200:
            raise serializers.ValidationError('Title should be no more than 200 characters')
        return value

'''User Game List'''
class UserGameEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGameEntry
        fields = ['games', 'status']
        
    def validate(self, data):
        user = self.context['request'].user 
        games = data['games']
        
        if not User.objects.filter(id=user.id).exists():
            raise serializers.ValidationError('User does not exist')
        
        if UserGameEntry.objects.filter(user=user, games=games).exists():
            raise serializers.ValidationError('This game is already in the list')
        
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user 
        games = validated_data['games']
        status = validated_data['status']
        
        entry = UserGameEntry(user=user, games=games, status=status)
        entry.save()
        return entry
