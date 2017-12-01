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
    context = {'user': user}
    to = [user.email]
    email.ActivationEmail(context=context).send(to)
