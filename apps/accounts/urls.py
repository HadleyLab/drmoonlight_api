from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from apps.accounts import viewsets


router = SimpleRouter()
router.register('resident', viewsets.ResidentViewSet)


urlpatterns = [
    url(r'^accounts/', include('djoser.urls')),
    url(r'^accounts/', include('djoser.urls.authtoken')),
    url(r'^accounts/', include(router.urls)),
]
