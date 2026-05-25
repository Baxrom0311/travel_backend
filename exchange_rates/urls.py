from django.urls import path
from .views import exchange_rates_view

urlpatterns = [
    path('exchange-rates/', exchange_rates_view, name='exchange-rates'),
]
