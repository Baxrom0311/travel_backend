from django.core.exceptions import ValidationError
from django.test import Client, TestCase

from .models import TransportRoute


class TransportApiTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')
        self.route = TransportRoute.objects.create(
            transport_type='taxi',
            icon='T',
            from_location_uz='Urganch aeroporti',
            to_location_uz='Xiva',
            duration_min=30,
            duration_max=40,
            price_min=30000,
            price_max=50000,
            description_uz='Taksi yonalishi',
        )

    def test_transport_detail_endpoint(self):
        response = self.client.get(f'/api/transport/{self.route.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], self.route.id)

    def test_transport_options_endpoint(self):
        response = self.client.get('/api/transport/options/')

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])
        self.assertIn({'value': 'taxi', 'label': 'Taksi'}, body['types'])
        self.assertEqual(body['price'], {'min': 30000, 'max': 50000})
        self.assertEqual(body['duration'], {'min': 30, 'max': 40})

    def test_invalid_transport_type_returns_400(self):
        response = self.client.get('/api/transport/?type=plane')

        self.assertEqual(response.status_code, 400)

    def test_unknown_transport_query_param_returns_400(self):
        for path in ['/api/transport/?foo=bar', '/api/transport/options/?foo=bar']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 400)

    def test_transport_range_validation(self):
        route = TransportRoute(
            transport_type='taxi',
            from_location_uz='A',
            to_location_uz='B',
            duration_min=60,
            duration_max=30,
            price_min=100,
            price_max=50,
            description_uz='Invalid route',
        )

        with self.assertRaises(ValidationError):
            route.clean()
