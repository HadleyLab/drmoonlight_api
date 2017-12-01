from apps.main.utils import async_send_mail


def get_user_info(user):
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'full_name': user.full_name,
        'username': user.username,
        'pk': user.pk,
    }


def process_resident_profile_filling(resident):
    from apps.accounts.models import AccountManager

    async_send_mail(
        'resident_profile_filled',
        list(AccountManager.objects.values_list('email', flat=True)),
        {
            'resident': get_user_info(resident),
        }
    )


def process_resident_approving(resident):
    async_send_mail(
        'resident_approved',
        resident.email,
        {
            'resident': get_user_info(resident),
        }
    )


def process_resident_rejecting(resident):
    async_send_mail(
        'resident_rejected',
        resident.email,
        {
            'resident': get_user_info(resident),
        }
    )
