from django.urls import path

from api.files.views import Delete, Upload

urlpatterns = [
    path('upload/', Upload.as_view(), name='upload'),
    path('delete/', Delete.as_view(), name='delete'),
]
