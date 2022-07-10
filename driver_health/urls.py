"""driver_health URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

from django.contrib.auth.models import User
from user_accounts.models import CustomUser
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user_accounts/api/views', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('user_accounts/', include('user_accounts.urls')),
    path('', include('home.urls')),
    path('careers/', include('careers.urls')),
    path('dhclients/', include('dhclients.urls')),
    path('companies/', include('companies.urls')),
    path('countries/', include('countries.urls')),
    path('about_us/', include('about_us.urls')),
    path('contact_us/', include('contact_us.urls')),
    path('gallery/', include('gallery.urls')),
]


if settings.DEBUG:
    urlpatterns +=[
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root':
                                             settings.MEDIA_ROOT,}),
    ]