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