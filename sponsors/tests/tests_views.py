from django.test import TestCase
from django.shortcuts import reverse
from .factories import SponsorFactory

class SponsorsTest(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("sponsors_page")

    def test_nosponsors(self):
        """make sure there are pictures on the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["sponsors"]), [])

    def test_sponsorsshow(self):
        """make sure if there are pictures, they are pictures on the page"""
        sponsor1 = SponsorFactory()
        sponsor2 = SponsorFactory()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["sponsors"]), [sponsor1, sponsor2])