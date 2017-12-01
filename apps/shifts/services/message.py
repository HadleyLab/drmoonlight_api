from apps.accounts.services.user import get_user_context
from apps.main.utils import async_send_mail
from apps.shifts.notifications import notify_message_created
from .shift import get_shift_context


def create_message(application, owner, text):
    from apps.shifts.models import Message

    if text:
        message = Message.objects.create(
            application=application, owner=owner, text=text)
        process_message_creation(message, notify=False)

        return message

    return None


def process_message_creation(message, notify=True):
    from .application import get_application_context, get_opposite_side

    if notify:
        notify_message_created(message)

        destination = get_opposite_side(message.application, message.owner)

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
                    'application': get_application_context(message.application),
                    'shift': get_shift_context(message.application.shift),
                }
            )
