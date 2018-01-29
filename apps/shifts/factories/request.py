from django.test import RequestFactory


class ExtendedRequestFactory(RequestFactory):
    def build_absolute_uri(self, path):
        return path
