from django.test import TestCase
from django.urls import reverse

class SimpleUserTests(TestCase):
    def test_login_page_status(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
