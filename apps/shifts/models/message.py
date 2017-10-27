from django.db import models

from apps.accounts.models import User
from apps.main.models import TimestampModelMixin
from .application import Application


class Message(TimestampModelMixin, models.Model):
    owner = models.ForeignKey(
        User,
        verbose_name='Owner'
    )
    application = models.ForeignKey(
        Application,
        verbose_name='Application'
    )
    message = models.TextField(
        verbose_name='Message'
    )

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
