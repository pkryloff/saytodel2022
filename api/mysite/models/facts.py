from django.db import models

from api.accounts.models.profile import User


class MyFacts(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    fact = models.CharField(max_length=128, null=True)
