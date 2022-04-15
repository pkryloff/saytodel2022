from django.db import models
from django.utils.translation import gettext_lazy

from api.accounts.models.profile import User


class Order(models.Model):
    class OrderStatuses(models.TextChoices):
        NEW = 'Новая', gettext_lazy('Новая')
        IN_PROGRESS = 'В работе', gettext_lazy('В работе')
        DONE = 'Выполнена', gettext_lazy('Выполнена')
        DECLINED = 'Отказ', gettext_lazy('Отказ')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, null=True)
    contact = models.CharField(max_length=64, null=True)
    status = models.CharField(max_length=16, choices=OrderStatuses.choices, default=OrderStatuses.NEW)
    comment = models.CharField(max_length=512, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
