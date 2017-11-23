from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from apps.shifts import viewsets


router = SimpleRouter()
router.register('shift', viewsets.ShiftViewSet)
router.register('application', viewsets.ApplicationViewSet)


urlpatterns = [
    url(r'^shifts/', include(router.urls)),
]
