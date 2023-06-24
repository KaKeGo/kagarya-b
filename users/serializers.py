from rest_framework import serializers

from django.contrib.sessions.models import Session
from django.utils import timezone

from .models import (
    User, Profile, Gender
)


'''Serializer for User'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
            write_only=True, 
            required=True,
            style={'input_type': 'password'}
        )
    confirm_password = serializers.CharField(
            write_only=True, 
            required=True, 
            style={'input_type': 'password'}
        )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def validate_password(self, value):
        min_length = 6
        max_length = 20
        
        if len(value) < min_length:
            raise serializers.ValidationError(f'Password must be longer then {min_length}')
        if len(value) > max_length:
             raise serializers.ValidationError(f'Password must be shorter then {max_length}')
        return  value
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError('Password do not match')
        
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

'''Serializer for User Profile'''
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    online_status = serializers.SerializerMethodField()
        
    class Meta:
        model = Profile
        fields = [
            'id', 'get_username', 'user', 'avatar', 'about', 
            'motto', 'gender', 'slug', 'online_status'
            ]
        read_only_fields = ['slug']
        
    def get_online_status(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            session_key = request.session.session_key
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            user_sessions = active_sessions.filter(session_key=session_key)
            return user_sessions.exists() and obj.user == request.user
        return False

'''Serializer for Gender'''
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']
