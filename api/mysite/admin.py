from django.contrib import admin

from api.mysite.models.facts import MyFacts
from api.mysite.models.site import MySite

admin.site.register(MySite)
admin.site.register(MyFacts)
