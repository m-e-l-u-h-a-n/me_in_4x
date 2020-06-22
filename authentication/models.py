from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars',null=True)
    # memories = models.ForeignKey(Memory, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print(instance)
    instance.profile.save()
