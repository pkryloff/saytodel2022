from django.db import models

from api.accounts.models.profile import User


class MySite(models.Model):
    class ColorOptions(models.TextChoices):
        BLUE = 'Blue'
        LIGHT_BlUE = 'LightBlue'
        GREEN = 'Green'
        PURPLE = 'Purple'
        RED = 'Red'
        ORANGE = 'Orange'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=2048, null=True)  # How about Markdown/HTML support?
    color = models.CharField(max_length=16, choices=ColorOptions.choices, default=ColorOptions.BLUE)
    name = models.CharField(max_length=128, null=True)  # ascii
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
