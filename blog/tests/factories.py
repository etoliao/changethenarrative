import factory 
import factory.fuzzy
from blog.models import Post 
from django.contrib.auth import get_user_model

class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.fuzzy.FuzzyText()
    last_name = factory.fuzzy.FuzzyText()
    username = factory.fuzzy.FuzzyText()

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "password"
        self.set_password(password)
        self.save()

    class Meta:
        model = get_user_model()

class PostFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    text = factory.fuzzy.FuzzyText()
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
