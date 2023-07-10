from django.contrib import admin

from .models import (
    TodoPlan, Todo, Task, TodoCategory
)


admin.site.register([TodoPlan, Todo, Task, TodoCategory])
