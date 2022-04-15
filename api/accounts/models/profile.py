from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)

    image_url = models.CharField(max_length=128, null=True)

    gender = models.CharField(max_length=16, null=True)
    phone = PhoneNumberField(null=True)
    address = models.CharField(max_length=256, null=True)
    occupation = models.CharField(max_length=64, null=True)
    inn = models.CharField(max_length=12, null=True)

    vk = models.CharField(max_length=128, null=True)
    instagram = models.CharField(max_length=128, null=True)
    facebook = models.CharField(max_length=128, null=True)
    website = models.CharField(max_length=128, null=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
