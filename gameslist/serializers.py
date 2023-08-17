from rest_framework import serializers

from .models import (
    GameList, Type, Category
)


#Anime Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

#Anime Type
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']
        
#Anime Serializer
class GamesListSerializer(serializers.ModelSerializer):
    anime_type = TypeSerializer(many=True)
    category = CategorySerializer(many=True)
    
    class Meta:
        model = GameList
        fields = [
                'id', 'cover', 'title', 'body', 'game_type',
                'category', 'average_raiting' 
            ]
