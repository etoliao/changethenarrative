from django.test import TestCase
from django.shortcuts import reverse
from pictures.tests.factories import PictureFactory

class PicturesTest(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("pictures_page")

    def test_nopictures(self):
        """checks if there are no pictures on the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["pictures"]), [])

    def test_picturesshow(self):
        """make sure if there are pictures, they are pictures on the page"""
        picture1 = PictureFactory()
        picture2 = PictureFactory()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["pictures"]), [picture1, picture2])