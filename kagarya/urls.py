from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('kakemin/', admin.site.urls),
    
    path('', include('home.urls')),
    path('accounts/', include('users.urls')),
    path('todo/', include('todo.urls')),
    
    #Lists
    path('anime/', include('animelist.urls')),
    path('manga/', include('mangalist.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
