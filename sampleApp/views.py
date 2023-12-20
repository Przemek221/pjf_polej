from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


from django.views.generic import ListView
from .models import Something
from .models import Post
from django.contrib import messages
from .forms import RegisterUserForm


# from django.contrib.auth.forms import UserCreationForm

class AllToDos(ListView):
    model = Something
    template_name = "sampleApp/index.html"


class loginPage(ListView):
    model = Something
    template_name = "sampleApp/login.html"


# class registerPage(ListView):
# model = Something
# model = User
# template_name = "sampleApp/register.html"


# def addusr(request):
#     if request.method == 'POST':
#         form = addUserForm(request.POST)
#         # nickname = request.POST['nickname']
#         # User.objects.create(nickname=form.nickname,password=form.password,role=User.Roles.USER)
#         # password = request.POST['passwd']
#         # if form.is_valid(addUserForm):
#         ysr = User(nickname=form.nickname, password=form.password, role=User.Roles.USER)
#         ysr.save()
#     else:
#         form = addUserForm()
#
#     return render(request, 'sampleApp/register.html', {"form": form})


# argument dla fcji, dla strony index html
sth = [
    {'number': 5, 'desc': 'sss'},
    {'number': 1, 'desc': 'ddd'}
]


def xxx(request):
    arg = {
        'title': 'abc',
        'object_list': sth
    }
    return render(request, 'sampleApp/index.html', arg)


def displayPosts(request):
    arg = {
        'title': 'abc',
        'posts': Post.objects.all()
    }
    return render(request, 'sampleApp/posts.html', arg)


# def przyklkad(request):
#     argument = {'klucz': "wartosc"}
#     # return render(request, 'sampleApp/register.html', argument)
#     return render(request, 'sampleApp/register.html', {'argument': 'wartosc'})


def registerUser(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"User {username} registered")
            return redirect('index')
    else:
        form = RegisterUserForm()
    return render(request, 'sampleApp/register.html', {'form': form, 'title': 'register'})
