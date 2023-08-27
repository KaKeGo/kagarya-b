from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, FileExtensionValidator
from django.contrib.auth import get_user_model

from PIL import Image


from .models import (
    GameList, Type, Category, UserGameEntry, GameDeveloper, Founder,
    Comment, CommentRaiting, Platform, PlatformCreator,
)

User = get_user_model()


'''Platform'''
class PlatformCreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformCreator
        fields = '__all__'
        
    def validate_photo(self, value):
        image = Image.open(value)
        width, height = image.size
        max_image_size = 20 * 1024 * 1024
        
        if width > 800 or height > 800:
            raise serializers.ValidationError('Image should be no more than 800x800 pixels')
        
        if value.size > max_image_size:
            raise serializers.ValidationError('Image file size should be no more than 20mb')

        return value

class PlatformListSerializer(serializers.ModelSerializer):
    creator = PlatformCreatorSerializer(many=True)
    
    class Meta:
        model = Platform
        fields = '__all__'

class PlatformCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['name', 'description', 'logo', 'creator', 'date_established']
        
    def validate_logo(self, value):
        image = Image.open(value)
        width, height = image.size
        max_image_size = 20 * 1024 * 1024
        
        if width > 800 or height > 800:
            raise serializers.ValidationError('Image should be no more than 800x800 pixels')
        
        if value.size > max_image_size:
            raise serializers.ValidationError('Image file size should be no more than 20mb')

        return value
    
    def create(self, validated_data):
        creators = validated_data.pop('creator', [])
        platform = Platform.objects.create(**validated_data)
        platform.creator.set(creators)
        return platform

'''Comments'''
class CommentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentRaiting
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    ratings = serializers.StringRelatedField(many=True, read_only=True)
    game = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ['user', 'game', 'text', 'ratings', 'formatted_created_at']

'''Founders'''
class Founder(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = '__all__'

'''GameDeveloper'''
class GameDeveloperSerializer(serializers.ModelSerializer):
    founders = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = GameDeveloper
        fields = '__all__'
        
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
    game_type = serializers.StringRelatedField(many=True)
    category = serializers.StringRelatedField(many=True)
    developer = serializers.StringRelatedField()
    platforms = serializers.StringRelatedField(many=True)
    comments = CommentSerializer(many=True)
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = GameList
        fields = [
            'id', 'cover', 'video', 'title', 'body', 'game_type',
            'category', 'average_rating', 'developer', 'platforms',
            'comments', 'tags', 'release_date',
        ]

class GameListCreateSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ])
    video = serializers.URLField(validators=[URLValidator()])
    
    class Meta:
        model = GameList
        fields = [
            'title', 'body', 'video', 'cover', 'game_type', 'category',
            'status', 'developer', 'platforms', 'tags', 'release_date',
        ]
        
    def validate_title(self, value):
        if len(value) <0:
            raise serializers.ValidationError('Title should be at least 2 characters')
        elif len(value) >200:
            raise serializers.ValidationError('Title should be no more than 200 characters')
        
        return value
    
    def validate_body(self, value):
        if len(value) < 30:
            raise serializers.ValidationError('Body should be at least 30 characters')
        elif len(value) > 1000:
            raise serializers.ValidationError('Body should be no more than 1000 characters')
        
        return value
    
    def validate_cover(self, value):
        image = Image.open(value)
        width, height = image.size
        if width > 800 or height > 800:
            raise serializers.ValidationError('Image dimensions should be no more than 800x800 pixels')
        
        max_image_size = 20 * 1024 * 1024
        if value.size > max_image_size:
            raise serializers.ValidationError('Image file size should be no more than 20mb')
        
        return value
    
    def validate_video(self, value):
        url_validator = URLValidator()
        try:
            url_validator(value)
        except ValidationError:
            raise serializers.ValidationError('Invalid video URL')
        
        return value

'''User Game List'''
class UserGameEntrySerializer(serializers.ModelSerializer):
    games = GamesListSerializer(read_only=True)
    
    class Meta:
        model = UserGameEntry
        fields = ['games', 'status', 'rating', 'note']
        
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
        note = validated_data['note']
        rating = validated_data.get('rating')
        
        entry = UserGameEntry(
            user=user, 
            games=games, 
            status=status,
            note=note,
            rating=rating,
            )
        entry.save() 
        
        return entry
