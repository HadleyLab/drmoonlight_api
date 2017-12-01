def async_send_mail(slug, to, context):
    from .tasks import send_mail

    send_mail.delay(slug, to, context)
