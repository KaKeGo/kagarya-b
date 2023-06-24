from django.contrib import admin

from .models import (
    ApiUrls, ApiCategory
)

# Register your models here.


admin.site.register([ApiUrls, ApiCategory])
