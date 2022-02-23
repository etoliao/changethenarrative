from django.test import TestCase
from django.shortcuts import reverse

class HomepageTest(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("homepage")

    def test_nothingshows(self):
        """if there is a blank page, that is wrong"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)