"""Fetch exchange rates from CBU API and store in DB."""
import logging
import urllib.request
import json

from django.core.management.base import BaseCommand
from django.utils import timezone

from exchange_rates.models import ExchangeRate

logger = logging.getLogger(__name__)

CBU_URL = 'https://cbu.uz/en/arkhiv-kursov-valyut/json/'
SUPPORTED = {'USD', 'RUB'}
FALLBACK = {'USD': 12500.0, 'RUB': 137.0}


class Command(BaseCommand):
    help = 'Update exchange rates from CBU API'

    def handle(self, *args, **options):
        # Check if rates were updated within the last hour
        latest = ExchangeRate.objects.order_by('-updated_at').first()
        if latest and (timezone.now() - latest.updated_at).total_seconds() < 3600:
            self.stdout.write('Rates are fresh (< 1 hour). Skipping.')
            return

        rates = self._fetch_cbu()
        if not rates:
            self.stdout.write(self.style.WARNING('CBU unavailable, using fallback rates.'))
            rates = FALLBACK

        for currency, rate_to_uzs in rates.items():
            ExchangeRate.objects.update_or_create(
                currency=currency,
                defaults={'rate_to_uzs': rate_to_uzs},
            )
            self.stdout.write(f'  {currency} = {rate_to_uzs} UZS')

        self.stdout.write(self.style.SUCCESS('Exchange rates updated.'))

    def _fetch_cbu(self):
        try:
            req = urllib.request.Request(CBU_URL, headers={'User-Agent': 'VisitKhorezm/1.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            rates = {}
            for item in data:
                code = item.get('Ccy', '')
                if code in SUPPORTED:
                    rates[code] = float(item['Rate'])
            return rates if rates else None
        except Exception as e:
            logger.warning(f'CBU fetch failed: {e}')
            return None
