from django.test import TestCase
from django.shortcuts import reverse

class HomepageTest(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("homepage")

    def test_nothingshows(self):
        """checks if there is nothing on the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)