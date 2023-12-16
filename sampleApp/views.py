from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import ListView
from .models import Something


class AllToDos(ListView):
    model = Something
    template_name = "sampleApp/index.html"


class loginPage(ListView):
    model = Something
    template_name = "sampleApp/login.html"


class registerPage(ListView):
    model = Something
    template_name = "sampleApp/register.html"
