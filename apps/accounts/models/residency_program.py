from django.db import models


class ResidencyProgram(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=255
    )

    class Meta:
        verbose_name = 'Residency program'
        verbose_name_plural = 'Residency programs'

    def __str__(self):
        return "{0}".format(self.name)
