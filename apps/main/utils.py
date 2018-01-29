from sorl.thumbnail import get_thumbnail


def async_send_mail(slug, to, context):
    from .tasks import send_mail

    send_mail.delay(slug, to, context)


def get_diff_in_hours(end, start):
    return int((end - start).total_seconds() / 3600)


def get_avatar_thumbnail(avatar, request):
    if avatar:
        return request.build_absolute_uri(get_thumbnail(avatar, '100x100',
                                          crop='center', quality=90).url)
    else:
        return request.build_absolute_uri(
            '/static/default-physician-avatar.png')
