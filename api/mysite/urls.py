from django.urls import path

from api.mysite.views.facts import Facts, ViewFacts
from api.mysite.views.site import Site, ViewSite

urlpatterns = [
    path('', Site.as_view(), name='mysite'),
    path('facts/', Facts.as_view(), name='facts'),
    path('facts/<str:name>/', ViewFacts.as_view(), name='viewfacts'),
    path('<str:name>/', ViewSite.as_view(), name='viewsite'),
]
