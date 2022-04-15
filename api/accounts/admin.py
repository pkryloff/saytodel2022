from django.contrib import admin

from api.accounts.models.gallery import Gallery
from api.accounts.models.pricelist import Pricelist
from api.accounts.models.profile import User

admin.site.register(User)
admin.site.register(Pricelist)
admin.site.register(Gallery)
