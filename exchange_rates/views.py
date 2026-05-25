from django.utils import timezone
from django.utils.cache import patch_cache_control
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ExchangeRate

FALLBACK_RATES = {'USD': 12500.0, 'RUB': 137.0}


@api_view(['GET'])
def exchange_rates_view(request):
    """GET /api/exchange-rates/ — returns rates with UZS as base."""
    rates = {}
    updated = None

    for er in ExchangeRate.objects.all():
        rates[er.currency] = float(1 / er.rate_to_uzs) if er.rate_to_uzs else 0
        if updated is None or er.updated_at > updated:
            updated = er.updated_at

    # Use fallback if DB empty
    if not rates:
        rates = {k: 1 / v for k, v in FALLBACK_RATES.items()}
        updated = timezone.now()

    response = Response({
        'base': 'UZS',
        'rates': rates,
        'updated': updated.isoformat() if updated else None,
    })
    patch_cache_control(response, public=True, max_age=3600)
    return response
