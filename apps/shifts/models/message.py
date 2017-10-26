from django.db import models

from apps.accounts.models import User
from .application import Application


class Message(models.Model):
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date created'
    )
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
