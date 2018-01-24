import os
from uuid import uuid4

from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class ClassNameUploadPath(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.path, instance.__class__.__name__, filename)


class AvatarField(models.ImageField):
    def __init__(self, **kwargs):
        kwargs['upload_to'] = kwargs.get('upload_to',
                                         ClassNameUploadPath('avatars'))
        super(AvatarField, self).__init__(**kwargs)
