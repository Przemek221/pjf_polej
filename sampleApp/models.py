from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import User


# Create your models here.

class Something(models.Model):
    number = models.IntegerField()
    desc = models.CharField(max_length=30)

    def __str__(self):
        return f"num: {self.number} | desc: {self.desc}"


class User(models.Model):
    class Roles(models.TextChoices):
        USER = "usr", "user"
        MODERATOR = "mod", "moderator"
        ADMIN = "adm", "admin"

    # nickname = models.CharField(
    #     max_length=30,
    #     unique=True
    # )
    # password = models.CharField(
    #     max_length=30
    # )
    role = models.CharField(
        max_length=3,
        choices=Roles.choices,
        default=Roles.USER,
    )


class Post(models.Model):
    content = models.TextField
    createdDate = models.DateTimeField
    reactionCounter = models.IntegerField
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class PostAttachment(models.Model):
    content = models.FileField
    creator = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField
    createdDate = models.DateTimeField
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE)


class Message(models.Model):
    content = models.TextField
    date = models.DateTimeField
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class MessageAttachment(models.Model):
    content = models.FileField
    creator = models.ForeignKey(Message, on_delete=models.CASCADE)
