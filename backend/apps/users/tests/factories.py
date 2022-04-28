import factory
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    registered_at = timezone.now()

    class Meta:
        model = 'users.User'
        django_get_or_create = ('email', )
