from apps.main.notifications import notify


def notify_user(user, event, payload):
    notify('user-{0}'.format(user.pk), event, payload)


def notify_users(users, event, payload):
    for user in users:
        notify_user(user, event, payload)
