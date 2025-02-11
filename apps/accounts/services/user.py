from contextlib import contextmanager

import pytz
from django.utils import timezone
from djoser import email


def get_user_context(user):
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'username': user.username,
        'pk': user.pk,
        'is_resident': user.is_resident,
        'is_scheduler': user.is_scheduler,
        'is_account_manager ': user.is_account_manager,
        'role': user.role,
    }


def process_user_creation(user):
    with localize_for_user(user):
        email.ActivationEmail(context={'user': user}).send([user.email])


@contextmanager
def localize_for_user(user):
    """
    Context manager which should be used to localize output for
    the concrete `user`.
    Actually it just changes local timezone to user's timezone
    """
    timezone.activate(pytz.timezone(user.timezone))
    yield
    timezone.deactivate()
