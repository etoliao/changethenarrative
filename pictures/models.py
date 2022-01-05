from django.conf import settings
from django.db import models

class Picture(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to="pictures/")

    def __str__(self):
        return self.description