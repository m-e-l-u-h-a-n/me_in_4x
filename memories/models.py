from django.db import models
from authentication.models import Profile
import os
# Create your models here.


def photo_upload_path(instance, filename):

    return os.path.join("user_{id}/images/{file}".format(id=instance.owner.id, file=filename))


def file_upload_path(instance, filename):

    return os.path.join("user_{id}/files/{file}".format(id=instance.owner.id, file=filename))


class Images(models.Model):
    image = models.ImageField(upload_to=photo_upload_path)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    context = models.CharField(max_length=155, default="",blank=True)

    def __str__(self):
        return self.context


class Files(models.Model):
    file = models.FileField(upload_to=file_upload_path)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    context = models.CharField(max_length=155, default="",blank=True)

    def __str__(self):
        return self.context


class Memory(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=254,blank=True,default="No title provided"),
    description = models.TextField(
        max_length=1500,blank=True, default="No description provided")
    relatedDate = models.DateTimeField(),
    relatedImages = models.ForeignKey(Images, on_delete=models.CASCADE),
    relatedFiles = models.ForeignKey(Files, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
