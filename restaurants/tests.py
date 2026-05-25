from django.test import TestCase, Client
from .models import Restaurant, Cuisine


def create_restaurant(**overrides):
    data = {
        'name': 'Xiva Osh',
        'city': 'khiva',
        'price_range': '$$',
        'rating': 4.5,
        'address': 'Xiva markazi',
        'latitude': 41.37,
        'longitude': 60.36,
        'description_uz': 'Test restoran',
    }
    data.update(overrides)
    return Restaurant.objects.create(**data)


class RestaurantListTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')
        self.cuisine = Cuisine.objects.create(name_uz='O\'zbek', name_en='Uzbek', name_ru='Узбекская')
        self.r1 = create_restaurant(name='Xiva Osh', is_featured=True)
        self.r1.cuisines.add(self.cuisine)
        self.r2 = create_restaurant(name='Urgench Kabob', city='urgench', rating=4.0)

    def test_list_returns_all(self):
        resp = self.client.get('/api/restaurants/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 2)

    def test_filter_by_city(self):
        resp = self.client.get('/api/restaurants/?city=khiva')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 1)

    def test_filter_by_cuisine(self):
        resp = self.client.get(f'/api/restaurants/?cuisine={self.cuisine.pk}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 1)

    def test_invalid_city_returns_400(self):
        resp = self.client.get('/api/restaurants/?city=tashkent')
        self.assertEqual(resp.status_code, 400)

    def test_unknown_param_returns_400(self):
        resp = self.client.get('/api/restaurants/?foo=bar')
        self.assertEqual(resp.status_code, 400)

    def test_ordering_validation(self):
        resp = self.client.get('/api/restaurants/?ordering=created_at')
        self.assertEqual(resp.status_code, 400)

    def test_valid_ordering(self):
        resp = self.client.get('/api/restaurants/?ordering=-rating')
        self.assertEqual(resp.status_code, 200)

    def test_search(self):
        resp = self.client.get('/api/restaurants/?search=Xiva')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['count'], 1)


class RestaurantDetailTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')
        self.restaurant = create_restaurant()

    def test_detail_returns_200(self):
        resp = self.client.get(f'/api/restaurants/{self.restaurant.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_detail_not_found(self):
        resp = self.client.get('/api/restaurants/99999/')
        self.assertEqual(resp.status_code, 404)


class RestaurantOptionsTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')

    def test_options_endpoint(self):
        resp = self.client.get('/api/restaurants/options/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data['success'])
        self.assertIn('cities', data)
        self.assertIn('price_ranges', data)

    def test_options_rejects_unknown_params(self):
        resp = self.client.get('/api/restaurants/options/?foo=bar')
        self.assertEqual(resp.status_code, 400)
