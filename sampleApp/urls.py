from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('', views.index, name='index')
    # path('', views.AllToDos.as_view(), name='index'),
    path('', views.xxx, name='index'),
    path('profile', views.profile, name='profile'),
    # path('home', views.display_posts, name='home'),
    path('home', views.DisplayPosts.as_view(), name='home'),


    # pk is the primary key of the current post, "int:" says that it can only contain an integer
    path('post/<int:pk>/', views.PostDetails.as_view(), name='post-detail'),


    # path('post/<int:pk>/', views.post_details, name='post-detail'),


    path('post/new/', views.CreatePost.as_view(), name='post-create'),


    # path('post-like/<int:pk>', views.post_like, name="post-like"),
    path('post-like/<int:pk>', views.post_like, name="post-like"),

    # variable must be called "pk" in this template
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post-update'),

    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),

    path('user/<str:username>/', views.DisplayUsersPosts.as_view(), name='user-posts'),

    # path('login', views.loginPage.as_view(), name='login'),
    path('login', auth_views.LoginView.as_view(template_name="sampleApp/login.html"), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name="sampleApp/logout.html"), name='logout'),
    path('register', views.register_user, name='register')
]
