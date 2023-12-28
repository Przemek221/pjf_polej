from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', views.index, name='index')
    # path('', views.AllToDos.as_view(), name='index'),
    path('', views.xxx, name='index'),
    path('profile', views.profile, name='profile'),
    # path('home', views.displayPosts, name='home'),
    path('home', views.DisplayPosts.as_view(), name='home'),


    # pk is the primary key of the current post, "int:" says that it can only contain an integer
    # path('post/<int:pk>/', views.PostDetails.as_view(), name='post-detail'),


    path('post-det/<int:post_id>/', views.postDetails, name='post-detail'),


    path('post/new/', views.CreatePost.as_view(), name='post-create'),

    # variable must be caled "pk" in this template
    path('post-det/<int:pk>/update/', views.UpdatePost.as_view(), name='post-update'),

    path('post-det/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),

    path('user/<str:username>/', views.DisplayUsersPosts.as_view(), name='user-posts'),

    # path('login', views.loginPage.as_view(), name='login'),
    path('login', auth_views.LoginView.as_view(template_name="sampleApp/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name="sampleApp/logout.html"), name='logout'),
    path('register', views.registerUser, name='register')
]
