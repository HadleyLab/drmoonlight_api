from celery import shared_task
from dbmail import send_db_mail
from django.conf import settings


@shared_task
def send_mail(slug, to, context):
    domain = context.get('domain') or getattr(settings, 'DOMAIN', '')
    protocol = context.get('protocol') or getattr(settings, 'PROTOCOL', 'http')
    site_name = context.get('site_name') or getattr(settings, 'SITE_NAME', '')

    common_context = {
        'domain': domain,
        'protocol': protocol,
        'site_name': site_name,
    }
    common_context.update(context)

    send_db_mail(slug, to, common_context, use_celery=False)
