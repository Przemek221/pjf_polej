from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index')
    path('', views.AllToDos.as_view(), name='index'),
    path('/login', views.loginPage.as_view(), name='login'),
    path('/register', views.registerPage.as_view(), name='register')
]
