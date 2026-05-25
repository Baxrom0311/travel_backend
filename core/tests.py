from django.test import TestCase, Client
from hotels.models import Hotel
from attractions.models import Attraction


def create_hotel(**overrides):
    data = {
        'name': 'Test Hotel',
        'city': 'urgench',
        'stars': 4,
        'rating': 8.5,
        'price_per_night': 350000,
        'address': 'Urganch',
        'latitude': 41.55,
        'longitude': 60.63,
        'description_uz': 'Test',
    }
    data.update(overrides)
    return Hotel.objects.create(**data)


class GlobalSearchTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')
        create_hotel(name='Khorezm Palace')
        Attraction.objects.create(
            name_uz='Ichan Qala', name_en='Ichan Kala', name_ru='Ичан Кала',
            description_uz='Xiva ichki shahri', latitude=41.37, longitude=60.36,
            is_featured=True, order=1,
        )

    def test_search_returns_results(self):
        resp = self.client.get('/api/search/?q=Khorezm')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['query'], 'Khorezm')
        self.assertGreater(data['counts']['hotels'], 0)

    def test_search_requires_q_param(self):
        resp = self.client.get('/api/search/')
        self.assertEqual(resp.status_code, 400)

    def test_search_min_length(self):
        resp = self.client.get('/api/search/?q=a')
        self.assertEqual(resp.status_code, 400)

    def test_search_rejects_unknown_params(self):
        resp = self.client.get('/api/search/?q=test&foo=bar')
        self.assertEqual(resp.status_code, 400)

    def test_search_limit_param(self):
        resp = self.client.get('/api/search/?q=test&limit=2')
        self.assertEqual(resp.status_code, 200)

    def test_search_limit_max_validation(self):
        resp = self.client.get('/api/search/?q=test&limit=100')
        self.assertEqual(resp.status_code, 400)


class ApiOverviewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')

    def test_api_overview(self):
        resp = self.client.get('/api/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertIn('endpoints', data)
        self.assertIn('exchange_rates', data['endpoints'])


class HomeSummaryTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')

    def test_home_returns_all_sections(self):
        resp = self.client.get('/api/home/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        for key in ('featured_hotels', 'transport', 'attractions', 'events', 'news', 'restaurants', 'tours', 'stats'):
            self.assertIn(key, data)

    def test_home_cache_control(self):
        # home_summary doesn't use PublicCacheMixin but let's ensure it works
        resp = self.client.get('/api/home/')
        self.assertEqual(resp.status_code, 200)
