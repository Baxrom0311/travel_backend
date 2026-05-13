from django.urls import path
from .views import get_site_settings, get_map_providers

urlpatterns = [
    path('', get_site_settings, name='site-settings'),
    path('map-providers/', get_map_providers, name='map-providers'),
]
