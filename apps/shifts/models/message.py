import os
from django.db import models
from sorl.thumbnail import get_thumbnail

from apps.main.models import TimestampModelMixin


IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'tiff', 'tif', 'r3d', 'ari', 'gif', 'bmp',
                    'png']


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
    text = models.TextField(
        verbose_name='Text'
    )
    attachment = models.FileField(
        blank=True, null=True
    )

    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name) if self.attachment else ''

    @property
    def extension(self):
        return self.attachment_name.split('.')[-1].lower()

    @property
    def thumbnail(self):
        if self.pk is None or self.attachment is None or \
                        self.extension not in IMAGE_EXTENSIONS:
            return None

        try:
            return get_thumbnail(self.attachment, '100x100', crop='center',
                                 quality=99, format='PNG')
        except Exception:
            return None

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return '{0}'.format(self.owner)
