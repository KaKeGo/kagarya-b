from rest_framework import serializers

from .models import (
    FilmsList, Type, Category
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
class FilmsListSerializer(serializers.ModelSerializer):
    anime_type = TypeSerializer(many=True)
    category = CategorySerializer(many=True)
    
    class Meta:
        model = FilmsList
        fields = [
                'id', 'cover', 'title', 'body', 'anime_type',
                'episodes', 'category', 'average_raiting' 
            ]
