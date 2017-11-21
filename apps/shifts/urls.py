from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from apps.shifts import viewsets


router = SimpleRouter()
router.register('shift', viewsets.ShiftViewSet)


urlpatterns = [
    url(r'^accounts/', include(router.urls)),
]
