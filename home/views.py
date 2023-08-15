from django.shortcuts import render, redirect

from .models import ApiCategory

from .utils import send_email_to_client
# Create your views here.

def send_email(request):
    send_email_to_client()
    return redirect('/')

def homeView(request):
    categorys = ApiCategory.objects.all()
    template = 'home/home.html'
    context = {
        'categorys': categorys,
    }
    return render(request, template, context)
