from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import (
    TodoPlanListSerializer,
)

from .models import (
    TodoPlan, Todo, Task, TodoCategory
)

# Create your views here.


class TodoPlanView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request):
        user = request.user
        todo_plan = TodoPlan.objects.filter(author=user)
        serializer = TodoPlanListSerializer(todo_plan, many=True)
        return Response(serializer.data)
