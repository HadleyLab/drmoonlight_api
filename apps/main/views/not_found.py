from django.views.generic.base import RedirectView


class NotFoundView(RedirectView):
    permanent = True
    url = '/#/not-found'


not_found_view = NotFoundView.as_view()
