from django.urls import path

from api.marketplace.views import Marketplace

urlpatterns = [
    path('', Marketplace.as_view(), name='marketplace'),
]
