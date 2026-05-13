from django.urls import path
from .views import subscribe, unsubscribe

urlpatterns = [
    path('subscribe/', subscribe, name='newsletter-subscribe'),
    path('unsubscribe/', unsubscribe, name='newsletter-unsubscribe'),
]
