from django.urls import path

from .views import (
    TodoPlanView,
    
    TodoDetailView,
    
    TaskDetailView,
)

app_name = 'todo'


urlpatterns = [
    path('plan/<slug>/', TodoPlanView.as_view(), name='plan'),
    
    path('<slug>/', TodoDetailView.as_view(), name='todo_detail'),
    
    path('task/<pk>/', TaskDetailView.as_view(), name='task_detail'),
]

