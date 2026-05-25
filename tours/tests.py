from django.test import TestCase, Client


class TourOrderingSecurityTest(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST='testserver')

    def test_invalid_ordering_is_ignored(self):
        """Ensure arbitrary ordering fields (e.g. user__password) are rejected."""
        resp = self.client.get('/api/tours/?ordering=user__password')
        self.assertEqual(resp.status_code, 400)

    def test_valid_ordering_accepted(self):
        resp = self.client.get('/api/tours/?ordering=price')
        self.assertEqual(resp.status_code, 200)

    def test_unknown_query_param_rejected(self):
        resp = self.client.get('/api/tours/?foo=bar')
        self.assertEqual(resp.status_code, 400)
