from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, PostAttachment


# creating profile of created user
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# saving profile while saving user
@receiver(post_save, sender=User)
def saveProfile(sender, instance, **kwargs):
    instance.userprofile.save()

# @receiver(post_delete, sender=PostAttachment)
# def delete_post_attachment(sender, instance, **kwargs):
