from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    User, Profile, Gender
)

from .serializers import (
    UserSerializer,
    ProfileSerializer,
    GenderSerializer,
)


class ProfileListView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
