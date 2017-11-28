from apps.main.notifications import notify


def notify_user(user, event, payload_fn):
    notify('user-{0}'.format(user.pk), event, payload_fn)
