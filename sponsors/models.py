from django.conf import settings
from django.db import models

class Sponsors(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to="sponsors/")

    def __str__(self):
        return self.description