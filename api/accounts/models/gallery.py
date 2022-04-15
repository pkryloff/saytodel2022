from django.db import models

from api.accounts.models.profile import User


class Gallery(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)

    # Album of images related to one job?
    # Link to the job on Pricelist and/or customer review?
    image_url = models.CharField(max_length=128, null=True)
