from apps.main.utils import async_send_mail
from .user import get_user_context


def process_resident_profile_filling(resident):
    from apps.accounts.models import AccountManager

    async_send_mail(
        'resident_profile_filled',
        list(AccountManager.objects.values_list('email', flat=True)),
        {
            'resident': get_user_context(resident),
        }
    )


def process_resident_approving(resident):
    async_send_mail(
        'resident_approved',
        resident.email,
        {
            'resident': get_user_context(resident),
        }
    )


def process_resident_rejecting(resident):
    async_send_mail(
        'resident_rejected',
        resident.email,
        {
            'resident': get_user_context(resident),
        }
    )
