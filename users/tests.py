from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class ToggleFavoriteValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='fav@test.com', password='testpass123')
        self.client = Client()
        resp = self.client.post('/api/auth/login/', {'email': 'fav@test.com', 'password': 'testpass123'}, content_type='application/json')
        self.token = resp.json().get('access', '')

    def test_missing_fields_returns_400(self):
        resp = self.client.post(
            '/api/auth/favorites/toggle/',
            {},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
        )
        self.assertEqual(resp.status_code, 400)

    def test_invalid_favorite_type_returns_400(self):
        resp = self.client.post(
            '/api/auth/favorites/toggle/',
            {'favorite_type': 'invalid_type', 'object_id': 1},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Invalid favorite_type', resp.json()['error'])

    def test_invalid_object_id_returns_400(self):
        resp = self.client.post(
            '/api/auth/favorites/toggle/',
            {'favorite_type': 'hotel', 'object_id': 'not_a_number'},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn('integer', resp.json()['error'])

    def test_valid_toggle_adds_favorite(self):
        resp = self.client.post(
            '/api/auth/favorites/toggle/',
            {'favorite_type': 'hotel', 'object_id': 1},
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {self.token}',
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()['action'], 'added')

    def test_toggle_twice_removes_favorite(self):
        payload = {'favorite_type': 'hotel', 'object_id': 1}
        self.client.post('/api/auth/favorites/toggle/', payload, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        resp = self.client.post('/api/auth/favorites/toggle/', payload, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['action'], 'removed')

    def test_requires_auth(self):
        resp = self.client.post('/api/auth/favorites/toggle/', {}, content_type='application/json')
        self.assertEqual(resp.status_code, 401)
