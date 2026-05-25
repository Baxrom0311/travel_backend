from django.test import Client, TestCase

from .models import Attraction


class AttractionApiTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')
        self.attraction = Attraction.objects.create(
            name_uz='Kalta Minor',
            description_uz='Xiva ramzi',
            latitude=41.378,
            longitude=60.363,
            is_featured=True,
            order=1,
        )

    def test_attraction_detail_endpoint(self):
        response = self.client.get(f'/api/attractions/{self.attraction.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.attraction.id)

    def test_attraction_options_endpoint(self):
        response = self.client.get('/api/attractions/options/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['counts'], {'total': 1, 'featured': 1})

    def test_featured_filter_accepts_false(self):
        Attraction.objects.create(
            name_uz='Tosh Darvoza',
            description_uz='Darvoza',
            latitude=41.3762,
            longitude=60.3601,
            is_featured=False,
            order=2,
        )

        response = self.client.get('/api/attractions/?featured=false')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertFalse(response.json()['results'][0]['is_featured'])

    def test_list_without_featured_filter_returns_all_attractions(self):
        Attraction.objects.create(
            name_uz='Tosh Darvoza',
            description_uz='Darvoza',
            latitude=41.3762,
            longitude=60.3601,
            is_featured=False,
            order=2,
        )

        response = self.client.get('/api/attractions/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_invalid_featured_filter_returns_400(self):
        response = self.client.get('/api/attractions/?featured=maybe')

        self.assertEqual(response.status_code, 400)

    def test_unknown_attraction_query_param_returns_400(self):
        for path in ['/api/attractions/?foo=bar', '/api/attractions/options/?foo=bar']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 400)
