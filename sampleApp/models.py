import os.path

from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


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

    def save(self, **kwargs):
        super().save(**kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)


class Post(models.Model):
    content = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    # reactionCounter = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, default=None, blank=True, related_name='post_like')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"content: {self.content} | creator: {self.creator} | id: {self.id}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.id})

    def number_of_likes(self):
        return self.likes.count()


def get_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"user_{instance.relatedPost.creator.id}/post_{instance.relatedPost.id}/{filename}"


class PostAttachment(models.Model):
    relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    attachment = models.FileField(upload_to=get_directory_path)

    def __str__(self):
        return f"post: {self.relatedPost.id} | attachment_name: {self.attachment.name}"

    @property
    def filename(self):
        return os.path.basename(self.attachment.name)


class Comment(models.Model):
    content = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    relatedPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"content: {self.content} | creator: {self.creator} | post: {self.relatedPost.content}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.relatedPost.id})
