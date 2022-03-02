import factory 
import factory.fuzzy
from sponsors.models import Sponsors

class SponsorFactory(factory.django.DjangoModelFactory):
    description = factory.fuzzy.FuzzyText()
    image = factory.django.ImageField()

    class Meta:
        model = Sponsors