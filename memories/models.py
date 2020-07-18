from django.db import models
from authentication.models import Profile
import os
# Create your models here.


def file_upload_path(instance, filename):

    return os.path.join("user_{id}/files/{file}".format(id=instance.owner.id, file=filename))


class Memory(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=254, blank=True, default="No title provided"),
    description = models.TextField(
        max_length=1500, blank=True, default="No description provided")
    relatedDate = models.DateField(blank=True, null=True),

    def __str__(self):
        return f'{self.title}'


class Files(models.Model):
    file = models.FileField(upload_to=file_upload_path)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, default = None)
    name = models.CharField(max_length=155, default="", blank=True)

    def __str__(self):
        return f'{self.name}'
