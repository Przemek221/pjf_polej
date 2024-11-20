from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('', views.DisplayPosts.as_view(), name='home'),
    # pk is the primary key of the current post, "int:" says that it can only contain an integer
    path('post/<int:pk>/', views.post_details, name='post-detail'),
    path('post/<int:pk>/<int:attachment_id>/', views.download_file, name='download'),
    path('post/<int:pk>/comment/', views.CreateComment.as_view(), name='comment'),
    path('post/<int:pk>/comment/<int:comment_id>/delete/', views.comment_delete, name="comment-delete"),
    path('post/new/', views.create_post, name='post-create'),
    path('post-like/<int:pk>/', views.post_like, name="post-like"),
    # variable must be called "pk" in this template
    path('post/<int:pk>/update/', views.UpdatePost.as_view(), name='post-update'),
    path('post/<int:pk>/update/attachment/<int:attachment_id>/delete/', views.attachment_delete,
         name='attachment-delete'),
    path('post/<int:pk>/delete/', views.PostDelete.as_view(), name='post-delete'),
    path('user/<str:username>/', views.DisplayUsersPosts.as_view(), name='user-posts'),
    path('login/', auth_views.LoginView.as_view(template_name="sampleApp/login.html"), name='login'),
    path('logout/', views.MyLogoutView.as_view(template_name="sampleApp/logout.html"), name='logout'),
    path('register/', views.register_user, name='register')
]
