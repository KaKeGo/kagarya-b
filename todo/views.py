from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import (
    TodoPlanListSerializer,
    TodoSerializer,
    TaskSerializer,
    CategorySerializer,
    
)

from .models import (
    TodoPlan, Todo, Task, TodoCategory
)

# Create your views here.

'''Plan Todo Views'''
@method_decorator(csrf_protect, name='dispatch')
class TodoPlanView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request):
        user = request.user
        todo_plan = TodoPlan.objects.filter(author=user)
        serializer = TodoPlanListSerializer(todo_plan, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''Todo Views'''
class TodoDetailView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request, slug):
        todo = get_object_or_404(Todo, slug=slug)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''Task Views'''
class TaskDetailView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def get(self, request, pk):
        task = get_object_or_404(Task, id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
