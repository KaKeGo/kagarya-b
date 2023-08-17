from rest_framework import serializers

from .models import (
    MangaList, Type, Category
)


'''Manga Category'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

'''Manga Type'''
class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ['id', 'name']

'''Manga Serializer'''
class MangaListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    manga_type = TypeSerializer(many=True)
    
    class Meta: 
        model = MangaList   
        fields = [
                'id', 'author', 'title', 'body', 'cover','manga_type', 
                'category', 'slug', 'average_raiting'
            ]
