from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', views.index, name='index')
    # path('', views.AllToDos.as_view(), name='index'),
    path('', views.xxx, name='index'),
    path('profile', views.profile, name='profile'),
    path('posts', views.displayPosts, name='posts'),
    # path('login', views.loginPage.as_view(), name='login'),
    path('login', auth_views.LoginView.as_view(template_name="sampleApp/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name="sampleApp/logout.html"), name='logout'),
    path('register', views.registerUser, name='register')
]
