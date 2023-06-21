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
