from rest_framework import serializers

from django.contrib.auth.models import User

from .models import (
    TodoPlan, Todo, Task, TodoCategory
)


'''Category Serializer'''
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCategory
        fields = ['id', 'name']

'''Task Serializer'''
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'completed']

'''Todo Serializers'''
class TodoSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    task = TaskSerializer(many=True)
    
    class Meta:
        model = Todo
        fields = [
                'id', 'name', 'description',
                'task', 'category', 'completed',
                'date_created', 'slug',
            ]

'''Todo Plan Serializers'''
class TodoPlanListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    todo = TodoSerializer(many=True)
    
    class Meta:
        model = TodoPlan
        fields = ['id', 'author', 'name', 'todo',]
        
    def get_author(self, obj):
        return obj.author.username
