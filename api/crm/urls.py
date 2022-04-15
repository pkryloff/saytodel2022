from django.urls import path

from api.crm.views.order import Order, OrderStatus

urlpatterns = [
    path('order/', Order.as_view(), name='order'),
    path('orderstatus/', OrderStatus.as_view(), name='orderstatus'),
]
