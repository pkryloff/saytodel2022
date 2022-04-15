import os

from django.db import models

from api.accounts.models.profile import User


def make_path(instance, filename):
    if instance.context:
        return os.path.join(instance.context, str(instance.owner.id), filename)
    else:
        return os.path.join('default', str(instance.owner.id), filename)


class Image(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=make_path, max_length=100)
