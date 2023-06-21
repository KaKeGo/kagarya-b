from rest_framework import serializers

from .models import (
    User, Profile, Gender
)

'''Serializer for User'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

'''Serializer for User Profile'''
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'about', 'motto', 'gender', 'slug']
        read_only_fields = ['slug']
        
'''Serializer for Gender'''
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']
