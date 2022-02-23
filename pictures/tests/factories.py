import factory 
import factory.fuzzy
from pictures.models import Picture

class PictureFactory(factory.django.DjangoModelFactory):
    description = factory.fuzzy.FuzzyText()
    image = factory.django.ImageField()

    class Meta:
        model = Picture