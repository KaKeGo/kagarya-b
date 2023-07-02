from rest_framework import serializers

from django.shortcuts import get_object_or_404
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

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name',]

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

class TodoDetailSerializer(serializers.ModelSerializer):
    task = TaskSerializer(many=True)
    
    class Meta:
        model = Todo
        fields = ['name', 'description', 'task', 'slug']
        
    def update(self, instance, validated_data):
        tasks_data = validated_data.pop('task', [])
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        
        for task_data in tasks_data:
            task_id = task_data.get('id')
            if task_id:
                task = get_object_or_404(Task, id=task_id, todo=instance)
                for key, value in task_data.items():
                    setattr(task, key, value)
                task.save()
                
        for task_data in tasks_data:
            task_id = task_data.get('id')
            if not task_id:
                task = Task.objects.create(todo=instance, **task_data)
                task.save()
        
        instance.task.set(Task.objects.filter(todo=instance))
        
        return instance

class TodoCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
            many=True, 
            queryset=TodoCategory.objects.all(), 
            slug_field='name'
        )
    
    class Meta:
        model = Todo
        fields = ['name', 'description', 'category', 'slug',]
        
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        todo = Todo.objects.create(**validated_data)
        todo.category.set(category_data)  
        return todo

'''Todo Plan Serializers'''
class TodoPlanListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    todo = TodoSerializer(many=True)
    
    class Meta:
        model = TodoPlan
        fields = ['id', 'author', 'name', 'todo', 'slug']
        
    def get_author(self, obj):
        return obj.author.username

class TodoPlanDetailSerializer(serializers.ModelSerializer):
    todo = TodoCreateSerializer(many=True)
    
    class Meta:
        model = TodoPlan
        fields = ['name', 'todo', 'slug']
    
    def update(self, instance, validated_data):
        todos_data = validated_data.pop('todo', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        
        for todo_data in todos_data:
            category_data = todo_data.pop('category', [])
            todo_id = todo_data.get('id')
            
            if todo_id:
                todo = get_object_or_404(Todo, id=todo_id, todo_plan=instance)
                for key, value in todo_data.items():
                    setattr(todo, key, value)
                todo.save()
                todo.category.set(category_data)
            else:
                todo = Todo.objects.create(todo_plan=instance, **todo_data)
                todo.category.set(category_data)
                instance.todo.add(todo)
        
        return instance

class TodoPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoPlan
        fields = ['name',]
        
    def create(self, vailidated_data):
        user = self.context['request'].user
        plan_todo = TodoPlan.objects.create(author=user, **vailidated_data)
        return plan_todo
