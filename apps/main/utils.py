def async_send_mail(slug, to, context):
    from .tasks import send_mail

    send_mail.delay(slug, to, context)


def get_diff_in_hours(end, start):
    return int((end - start).total_seconds() / 3600)
