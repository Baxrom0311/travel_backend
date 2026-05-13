from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.cache import cache
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings

from .models import Amenity, ContactMessage, Hotel, HotelImage
from attractions.models import Attraction
from transport.models import TransportRoute


def create_hotel(**overrides):
    data = {
        'name': 'Khorezm Palace Hotel',
        'city': 'urgench',
        'stars': 4,
        'rating': 8.8,
        'price_per_night': 350000,
        'address': 'Urganch',
        'latitude': 41.5504,
        'longitude': 60.6301,
        'description_uz': 'Test description',
    }
    data.update(overrides)
    return Hotel.objects.create(**data)


class BackendSmokeTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')

    def test_public_endpoints_return_json(self):
        for path in ['/health/', '/api/', '/api/home/', '/api/amenities/', '/api/hotels/', '/api/hotels/stats/', '/api/hotels/options/']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response['content-type'], 'application/json')

    def test_health_check_reports_database_status(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['database'], 'ok')

    def test_invalid_hotel_filters_return_400(self):
        invalid_queries = [
            '/api/hotels/?city=nukus',
            '/api/hotels/?stars=9',
            '/api/hotels/?min_price=900&max_price=100',
            '/api/hotels/?ordering=created_at',
            '/api/hotels/?foo=bar',
        ]

        for path in invalid_queries:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 400)

    def test_hotels_page_size_query_param(self):
        for i in range(3):
            create_hotel(name=f'Hotel {i}', rating=8 + i / 10)

        response = self.client.get('/api/hotels/?page_size=2')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)
        self.assertEqual(len(response.json()['results']), 2)

    def test_hotels_without_featured_filter_returns_all_hotels(self):
        create_hotel(name='Featured hotel', is_featured=True, rating=9.1)
        create_hotel(name='Regular hotel', is_featured=False, rating=8.9)

        response = self.client.get('/api/hotels/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)

    def test_hotel_options_include_filter_metadata(self):
        amenity = Amenity.objects.create(
            name_uz='WiFi',
            name_en='WiFi',
            name_ru='WiFi',
            icon='W',
        )
        create_hotel(price_per_night=250000)
        create_hotel(name='Second Hotel', price_per_night=500000, rating=9.1)

        response = self.client.get('/api/hotels/options/')

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])
        self.assertEqual(body['price'], {'min': 250000, 'max': 500000})
        self.assertIn({'value': 'urgench', 'label': 'Urganch'}, body['cities'])
        self.assertEqual(body['amenities'][0]['id'], amenity.id)

    def test_hotels_can_be_filtered_by_amenity(self):
        wifi = Amenity.objects.create(name_uz='WiFi', name_en='WiFi', name_ru='WiFi', icon='W')
        pool = Amenity.objects.create(name_uz='Pool', name_en='Pool', name_ru='Pool', icon='P')
        wifi_hotel = create_hotel(name='WiFi Hotel', rating=9.0)
        pool_hotel = create_hotel(name='Pool Hotel', rating=8.8)
        wifi_hotel.amenities.add(wifi)
        pool_hotel.amenities.add(pool)

        response = self.client.get(f'/api/hotels/?amenity={wifi.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['id'], wifi_hotel.id)

    def test_unknown_query_params_on_metadata_endpoints_return_400(self):
        for path in ['/api/amenities/?foo=bar', '/api/hotels/options/?foo=bar']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 400)

    def test_home_summary_returns_limited_homepage_data(self):
        create_hotel(name='Featured 1', is_featured=True, rating=9.5)
        create_hotel(name='Featured 2', is_featured=True, rating=9.1)
        create_hotel(name='Regular', is_featured=False, rating=8.5)
        TransportRoute.objects.create(
            transport_type='taxi',
            from_location_uz='Urganch aeroporti',
            to_location_uz='Xiva',
            duration_min=30,
            duration_max=40,
            price_min=30000,
            price_max=50000,
            description_uz='Taksi yonalishi',
        )
        Attraction.objects.create(
            name_uz='Kalta Minor',
            description_uz='Xiva ramzi',
            latitude=41.378,
            longitude=60.363,
            is_featured=True,
            order=1,
        )

        response = self.client.get('/api/home/?hotel_limit=1&transport_limit=1&attraction_limit=1')

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])
        self.assertEqual(body['stats']['total_hotels'], 3)
        self.assertEqual(len(body['featured_hotels']), 1)
        self.assertEqual(len(body['transport']), 1)
        self.assertEqual(len(body['attractions']), 1)

    def test_home_summary_rejects_unknown_and_invalid_params(self):
        for path in ['/api/home/?foo=bar', '/api/home/?hotel_limit=0']:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 400)


class ContactEndpointTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(HTTP_HOST='testserver')

    def test_contact_validation_errors_are_returned(self):
        response = self.client.post(
            '/api/contact/',
            {'name': 'A', 'email': 'not-email', 'message': 'short'},
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()['success'])
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_contact_endpoint_is_rate_limited(self):
        payload = {
            'name': 'Ali',
            'email': 'ali@example.com',
            'message': 'Bu test xabari yetarlicha uzun.',
        }

        for _ in range(5):
            self.assertEqual(self.client.post('/api/contact/', payload, content_type='application/json').status_code, 201)
        self.assertEqual(self.client.post('/api/contact/', payload, content_type='application/json').status_code, 429)


class ImportHotelPhotosCommandTests(TestCase):
    def test_import_uses_supplied_source_directory(self):
        hotel = create_hotel()

        with TemporaryDirectory() as source_dir, TemporaryDirectory() as media_dir:
            source = Path(source_dir)
            hotel_dir = source / 'Urgench' / 'Khorezm Palace Hotel'
            hotel_dir.mkdir(parents=True)
            (hotel_dir / 'cover.jpg').write_bytes(b'fake image content')

            with override_settings(MEDIA_ROOT=Path(media_dir)):
                output = StringIO()
                call_command('import_hotel_photos', source=str(source), stdout=output)

        image = HotelImage.objects.get(hotel=hotel)
        self.assertEqual(image.image.name, f'hotels/{hotel.id}_cover.jpg')
        self.assertTrue(image.is_cover)


class HotelImageConstraintTests(TestCase):
    def test_only_one_cover_image_is_allowed_per_hotel(self):
        hotel = create_hotel()
        HotelImage.objects.create(hotel=hotel, image='hotels/one.jpg', is_cover=True)

        with self.assertRaises(IntegrityError), transaction.atomic():
            HotelImage.objects.create(hotel=hotel, image='hotels/two.jpg', is_cover=True)
