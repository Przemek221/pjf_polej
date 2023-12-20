from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index')
    # path('', views.AllToDos.as_view(), name='index'),
    path('', views.xxx, name='index'),
    path('posts', views.displayPosts, name='posts'),
    path('login', views.loginPage.as_view(), name='login'),
    path('register', views.registerUser, name='register')
]
