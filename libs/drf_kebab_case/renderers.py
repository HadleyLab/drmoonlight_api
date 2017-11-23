from rest_framework import renderers

from .utils import kebabize


class KebabCaseJSONRenderer(renderers.JSONRenderer):
    def render(self, data, *args, **kwargs):
        return super(KebabCaseJSONRenderer, self).render(
            kebabize(data), *args, **kwargs
        )
