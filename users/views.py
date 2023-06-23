from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import (
    User, Profile, Gender
)

from .serializers import (
    UserCreateSerializer,
    
    ProfileSerializer,
    
    GenderSerializer,
)

'''
To get token
'''
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request):
        return Response({'Success': 'CSRFToken cookie set'})

'''
Profile Views
'''
@method_decorator(csrf_protect, name='dispatch')
class ProfileListView(APIView):
    '''Users profile list'''
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

'''
User Views
'''
@method_decorator(csrf_protect, name='dispatch')
class UserProfileDetailView(APIView):
    '''User Profile Detail'''
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request, slug):
        profile = Profile.objects.filter(slug=slug)
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegisterView(APIView):
    '''Register User'''
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    '''Login User'''
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
