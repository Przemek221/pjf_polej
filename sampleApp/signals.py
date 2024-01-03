import logging
import os

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile, PostAttachment
from pathlib import Path


# creating profile of created user
@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# saving profile while saving user
@receiver(post_save, sender=User)
def saveProfile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_delete, sender=PostAttachment)
def delete_post_attachment(sender, instance, **kwargs):
    if instance.attachment is not None:
        if os.path.isfile(instance.attachment.path):
            logger = logging.getLogger(__name__)
            file_path = Path(instance.attachment.path)

            instance.attachment.close()
            os.remove(file_path)
            try:
                os.rmdir(file_path.parent.absolute())
            except:
                logger.warning("***folder is not empty or doesn't exist***")
            else:
                logger.info("***deleted successfully***")
