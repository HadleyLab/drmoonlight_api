from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter
from djoser import views as djoser_views

from apps.accounts import viewsets, views


router = SimpleRouter()
router.register('resident', viewsets.ResidentViewSet)
router.register('scheduler', viewsets.SchedulerViewSet)


urlpatterns = [
    url(
        r'^accounts/activate/$',
        djoser_views.ActivationView.as_view(),
        name='user_activate'
    ),
    url(
        r'^accounts/password/reset/$',
        djoser_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    url(
        r'^accounts/password/reset/confirm/$',
        djoser_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    url(r'^accounts/', include('djoser.urls.authtoken')),
    url(r'^accounts/', include(router.urls)),
    url(r'^accounts/me/', views.MeView.as_view()),
]
