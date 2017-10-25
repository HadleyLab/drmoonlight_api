from django.db import models


class Speciality(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )

    class Meta:
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'
