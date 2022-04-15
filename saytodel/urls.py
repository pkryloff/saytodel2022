"""
Samodelkin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from Samodelkin.settings import USE_S3
from Samodelkin.swagger import CustomOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title='Samodelkin`s API',
        default_version='v1',
        description='Samodelkin is a service that provides a set of tools '
                    'for promoting your business and finding clients.',
    ),
    public=True,
    generator_class=CustomOpenAPISchemaGenerator,
    permission_classes=(permissions.AllowAny,),
)


def index(request):
    return HttpResponse('Greetings from Samodelkin`s server!\n')


def api_index(request):
    return HttpResponse('Greetings from Samodelkin`s API!\n')


token_urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
]

api_urlpatterns = [
    path('', api_index, name='api-index'),
    path('token/', include(token_urlpatterns), name='tokens'),
    path('auth/', include('rest_registration.api.urls'), name='auth'),
    path('accounts/', include('api.accounts.urls'), name='accounts'),
    path('files/', include('api.files.urls'), name='files'),
    path('mysite/', include('api.mysite.urls'), name='mysite'),
    path('crm/', include('api.crm.urls'), name='crm'),
    path('marketplace/', include('api.marketplace.urls'), name='marketplace'),
]

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    re_path('^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path('^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path('^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include(api_urlpatterns), name='API'),
]

urlpatterns += staticfiles_urlpatterns()

if not USE_S3:
    urlpatterns += static(settings.MEDIA_FOLDER, document_root=settings.MEDIA_ROOT)
