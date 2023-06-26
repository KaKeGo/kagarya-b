from django.urls import path

from .views import (
    TodoPlanView,
)

app_name = 'todo'


urlpatterns = [
    path('plan/', TodoPlanView.as_view(), name='todo-plan'),
]

