from django.db import models

from api.accounts.models.profile import User


class Pricelist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True)
    price = models.CharField(max_length=128, null=True)
    description = models.TextField(null=True)  # How about Markdown/HTML support?
