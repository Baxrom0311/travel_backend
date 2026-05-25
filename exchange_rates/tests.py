from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from io import StringIO
from unittest.mock import patch
from exchange_rates.models import ExchangeRate


class ExchangeRateModelTest(TestCase):
    def test_create_rate(self):
        er = ExchangeRate.objects.create(currency='USD', rate_to_uzs=12500.0)
        self.assertIn('USD', str(er))
        self.assertIn('12500', str(er))


class ExchangeRateViewTest(TestCase):
    def test_fallback_when_empty(self):
        resp = self.client.get(reverse('exchange-rates'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['base'], 'UZS')
        self.assertIn('USD', data['rates'])
        self.assertIn('RUB', data['rates'])

    def test_returns_db_rates(self):
        ExchangeRate.objects.create(currency='USD', rate_to_uzs=12600.0)
        ExchangeRate.objects.create(currency='RUB', rate_to_uzs=140.0)
        resp = self.client.get(reverse('exchange-rates'))
        data = resp.json()
        self.assertAlmostEqual(data['rates']['USD'], 1 / 12600.0, places=8)
        self.assertAlmostEqual(data['rates']['RUB'], 1 / 140.0, places=8)

    def test_cache_control_header(self):
        resp = self.client.get(reverse('exchange-rates'))
        self.assertIn('max-age=3600', resp.get('Cache-Control', ''))


class UpdateRatesCommandTest(TestCase):
    @patch('exchange_rates.management.commands.update_rates.Command._fetch_cbu')
    def test_uses_fallback_when_cbu_unavailable(self, mock_fetch):
        mock_fetch.return_value = None
        out = StringIO()
        call_command('update_rates', stdout=out)
        self.assertTrue(ExchangeRate.objects.filter(currency='USD').exists())
        self.assertTrue(ExchangeRate.objects.filter(currency='RUB').exists())

    @patch('exchange_rates.management.commands.update_rates.Command._fetch_cbu')
    def test_stores_cbu_rates(self, mock_fetch):
        mock_fetch.return_value = {'USD': 12700.0, 'RUB': 142.0}
        out = StringIO()
        call_command('update_rates', stdout=out)
        usd = ExchangeRate.objects.get(currency='USD')
        self.assertEqual(float(usd.rate_to_uzs), 12700.0)

    @patch('exchange_rates.management.commands.update_rates.Command._fetch_cbu')
    def test_skips_when_fresh(self, mock_fetch):
        ExchangeRate.objects.create(currency='USD', rate_to_uzs=12500.0)
        out = StringIO()
        call_command('update_rates', stdout=out)
        mock_fetch.assert_not_called()
        self.assertIn('fresh', out.getvalue())
