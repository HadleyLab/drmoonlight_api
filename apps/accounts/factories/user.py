from factory import DjangoModelFactory, PostGenerationMethodCall, Faker

from apps.accounts.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True
