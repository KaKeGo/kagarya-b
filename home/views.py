from django.shortcuts import render

from .models import ApiCategory

# Create your views here.


def homeView(request):
    categorys = ApiCategory.objects.all()
    template = 'home/home.html'
    context = {
        'categorys': categorys,
    }
    return render(request, template, context)
