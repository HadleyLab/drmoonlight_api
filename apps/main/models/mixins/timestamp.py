from django.db import models


class TimestampModelMixin(object):
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date created'
    )
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Date modified'
    )
