from django.conf.urls import url, include

from apps.main import views


urlpatterns = [
    url(r'^statistics/', views.statistics),
]
