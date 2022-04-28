from django.urls import path
from django.contrib import admin
from django.contrib.auth import logout

from django.conf.urls import include

from config.api import urlpatterns as api_urlpatterns


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls, name='admin'),
    path('logout/', logout, {'next_page': '/'}, name='logout'),
    path('api/', include(api_urlpatterns)),
    path('api/geodata/', include('apps.geodata.urls', namespace='geodata')),
]
