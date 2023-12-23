from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Something(models.Model):
    number = models.IntegerField()
    desc = models.CharField(max_length=30)

    def __str__(self):
        return f"num: {self.number} | desc: {self.desc}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return f"Profile of the user: {self.user.username}"

    def save(self):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)


class Post(models.Model):
    content = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    reactionCounter = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"content: {self.content} | creator: {self.creator}"

# class PostAttachment(models.Model):
#     content = models.FileField
#     creator = models.ForeignKey(Post, on_delete=models.CASCADE)


# class Comment(models.Model):
#     content = models.TextField
#     createdDate = models.DateTimeField(auto_now_add=True)
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE)


# class Message(models.Model):
#     content = models.TextField
#     createdDate = models.DateTimeField(auto_now_add=True)
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)


# class MessageAttachment(models.Model):
#     content = models.FileField
#     creator = models.ForeignKey(Message, on_delete=models.CASCADE)
