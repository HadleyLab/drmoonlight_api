from factory import DjangoModelFactory
from rest_framework.authtoken.models import Token


class TokenFactory(DjangoModelFactory):
    class Meta:
        model = Token
