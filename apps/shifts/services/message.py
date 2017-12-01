from apps.accounts.services.user import get_user_context
from apps.main.utils import async_send_mail
from apps.shifts.notifications import notify_message_created
from apps.shifts.services.shift import get_shift_context


def get_opposite_side(message):
    """
    Returns opposite side of message owner
    """
    if message.owner.is_resident:
        return message.application.shift.owner
    else:
        return message.application.owner


def process_message_creation(message, notify=True):
    if notify:
        notify_message_created(message)

        destination = get_opposite_side(message)

        mail_notification_enabled = destination.is_scheduler or (
            destination.is_resident and
            destination.notification_new_messages
        )

        if mail_notification_enabled:
            async_send_mail(
                'message_created',
                destination.email,
                {
                    'source': get_user_context(message.owner),
                    'destination': get_user_context(destination),
                    'text': message.text,
                    'application': {
                        'pk': message.application.pk,
                    },
                    'shift': get_shift_context(message.application.shift),
                }
            )
