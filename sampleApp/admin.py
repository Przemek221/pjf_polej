from django.contrib import admin

# Register your models here.
from .models import Something
from .models import Post


admin.site.register(Something)
admin.site.register(Post)
