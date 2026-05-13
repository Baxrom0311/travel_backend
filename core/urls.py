from django.urls import path
from .views import home_summary, api_overview, global_search

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('home/', home_summary, name='home-summary'),
    path('search/', global_search, name='global-search'),
]
