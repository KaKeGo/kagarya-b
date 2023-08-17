from rest_framework import serializers

from .models import (
    BooksList, Type, Category
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
class BooksListSerializer(serializers.ModelSerializer):
    books_type = TypeSerializer(many=True)
    category = CategorySerializer(many=True)
    
    class Meta:
        model = BooksList
        fields = [
                'id', 'cover', 'title', 'body', 'books_type',
                'toms', 'category', 'average_raiting' 
            ]
