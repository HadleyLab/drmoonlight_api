from factory import DjangoModelFactory

from apps.shifts.models import Message


class MessageFactory(DjangoModelFactory):
    class Meta:
        model = Message
