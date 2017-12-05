from apps.main.utils import async_send_mail
from .user import get_user_context, localize_for_user


def get_context(resident):
    return {
        'resident': get_user_context(resident),
    }


def process_resident_profile_filling(resident):
    from apps.accounts.models import AccountManager

    with localize_for_user(resident):
        async_send_mail(
            'resident_profile_filled',
            list(AccountManager.objects.values_list('email', flat=True)),
            get_context(resident)
        )


def process_resident_approving(resident):
    with localize_for_user(resident):
        async_send_mail(
            'resident_approved',
            resident.email,
            get_context(resident)
        )


def process_resident_rejecting(resident):
    with localize_for_user(resident):
        async_send_mail(
            'resident_rejected',
            resident.email,
            get_context(resident)
        )
