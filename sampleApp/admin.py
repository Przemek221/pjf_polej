from django.contrib import admin

# Register your models here.
from .models import Something, Post, UserProfile

admin.site.register(Something)
admin.site.register(UserProfile)
admin.site.register(Post)
