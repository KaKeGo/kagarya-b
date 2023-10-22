from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.shortcuts import redirect

from urllib.parse import urlencode

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .custom_permissions import UserRolePermissionFactory

from .models import User, Roles
from .profile_model import (
    Profile, Gender
)

from .serializers import (
    UserCreateSerializer,
    ProfileSerializer,
    GenderSerializer,
    RoleListSerializer, RoleCreateSerializer,
)

'''
To get token
'''
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'CSRFToken': csrf_token})

'''
Auth user
'''
class UserAuthCheckView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try: 
                profile = user.profile
                user_slug = profile.slug
                roles = [role.title for role in user.roles.all()]
            except Profile.DoesNotExist:
                return Response({'Message': 'Slug not exists.'})
            return Response({
                'is_authenticated': True,
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'slug': user_slug,
                    'roles': roles,
                }
            })
        else:
            return Response({'is_authenticated': False})

'''
Profile Views
'''
# @method_decorator(csrf_protect, name='dispatch')
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

@method_decorator(csrf_protect, name='dispatch')
class UserRegisterView(APIView):
    '''Register User'''
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = default_token_generator.make_token(user)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))

            activation_link = f'https://www.kagarya.com/accounts/activate/{uid64}/{token}/'
            
            subject = 'Account activation'
            message = render_to_string(
                'users/activation_email.html', 
                {
                    'activation_link': activation_link,
                    'username': user.username,
                }
                )
            send_mail(
                subject, 
                strip_tags(message), 
                'adress@example.com', 
                [user.email],
                html_message=message
                )
            
            return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateAccountView(APIView):
    '''Activate User Account'''
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request, uidb64, token):
        try:
            uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_active:
                return redirect('https://www.kagarya.com/accounts/activated')
                # return Response({'error': 'Account is already activated'}, status=status.HTTP_400_BAD_REQUEST)
                
            user.is_active = True
            user.save()
            return redirect('https://www.kagarya.com/accounts/activate/success')
            # return Response({'success': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return redirect('https://www.kagarya.com/accounts/activate/error')
            # return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(APIView):
    '''Login User'''
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'success': 'User logged in successfully'})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(csrf_protect, name='dispatch')
class UserLogoutView(APIView):
    '''Logout User'''
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request, *args, **kwargs):
        logout(request)
        response = Response({'success': 'User logged out successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('sessionid')
        response.delete_cookie('csrftoken')
        return response

'''Roles'''
class RoleListView(APIView):
    def get(self, request):
        roles = Roles.objects.all()
        serializer = RoleListSerializer(roles, many=True)
        return Response(serializer.data)

@method_decorator(csrf_protect, name='dispatch')
class RoleCreateView(APIView):
    permission_classes = [
        UserRolePermissionFactory(['Admin'])()
    ]

    def post(self, request):
        serializer = RoleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class RoleUpdateView(APIView):
    permission_classes = [
        UserRolePermissionFactory(['Admin'])()
    ]

    def get_object(self, pk):
        try:
            return Roles.objects.get(pk=pk)
        except Roles.DoesNotExist:
            return Response({'message': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        role = self.get_object(pk)
        serializer = RoleListSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_protect, name='dispatch')
class RoleDeleteView(APIView):
    permission_classes = [
        UserRolePermissionFactory(['Admin'])()
    ]

    def get_object(self, pk):
        try:
            return Roles.objects.get(pk=pk)
        except Roles.DoesNotExist:
            return Response({'message': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
