from django.urls import path

from .views import (
    TodoPlanView, TodoPlanDetailView, TodoPlanCreateView,
    
    TodoDetailView, TodoCreateView,
    
    TaskDetailView,
)


app_name = 'todo'


urlpatterns = [
    path('plan/create/', TodoPlanCreateView.as_view(), name='plan_create'),
    path('create/', TodoCreateView.as_view(), name='todo_create'),
    
    path('plan/', TodoPlanView.as_view(), name='plan_list'),
    path('plan/<slug>/', TodoPlanDetailView.as_view(), name='plan'),
    
    path('<slug>/', TodoDetailView.as_view(), name='todo_detail'),
    
    path('task/<pk>/', TaskDetailView.as_view(), name='task_detail'),
]

