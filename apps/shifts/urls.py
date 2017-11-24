from django.conf.urls import url, include
from rest_framework_nested import routers

from apps.shifts import viewsets


router = routers.SimpleRouter()
router.register('shift', viewsets.ShiftViewSet)
router.register('application', viewsets.ApplicationViewSet)

application_nested_router = routers.NestedSimpleRouter(
    router, 'application', lookup='application'
)
application_nested_router.register('message', viewsets.MessageViewSet)


urlpatterns = [
    url(r'^shifts/', include(router.urls)),
    url(r'^shifts/', include(application_nested_router.urls)),
]
