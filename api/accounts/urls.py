from django.urls import path

from api.accounts.views.gallery import Gallery, ViewGallery
from api.accounts.views.pricelist import Pricelist, ViewPricelist
from api.accounts.views.profile import Profile, ViewProfile

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('gallery/', Gallery.as_view(), name='gallery'),
    path('pricelist/', Pricelist.as_view(), name='pricelist'),
    path('view/profile/<int:user_id>', ViewProfile.as_view(), name='viewprofile'),
    path('view/gallery/<int:user_id>', ViewGallery.as_view(), name='viewgallery'),
    path('view/pricelist/<int:user_id>', ViewPricelist.as_view(), name='viewprofile'),
]
