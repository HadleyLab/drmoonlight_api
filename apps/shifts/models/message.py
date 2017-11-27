from django.db import models

from apps.main.models import TimestampModelMixin


class Message(TimestampModelMixin, models.Model):
    owner = models.ForeignKey(
        'accounts.User',
        related_name='messages',
        verbose_name='Owner'
    )
    application = models.ForeignKey(
        'shifts.Application',
        related_name='messages',
        verbose_name='Application'
    )
    message = models.TextField(
        verbose_name='Message'
    )

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return "{0}".format(self.owner)
