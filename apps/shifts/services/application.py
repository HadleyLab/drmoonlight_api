from apps.accounts.services.user import get_user_context
from apps.main.utils import async_send_mail
from apps.shifts.notifications import notify_application_state_changed
from .shift import get_shift_context


def get_application_context(application):
    return {
        'pk': application.pk,
    }


def process_application(application):
    async_send_mail(
        'application_created',
        application.shift.owner.email,
        {
            'scheduler': get_user_context(application.shift.owner),
            'resident': get_user_context(application.owner),
            'application': get_application_context(application),
            'shift': get_shift_context(application.shift),
        }
    )


def process_invitation(application):
    async_send_mail(
        'invitation_created',
        application.owner.email,
        {
            'scheduler': get_user_context(application.shift.owner),
            'resident': get_user_context(application.owner),
            'application': get_application_context(application),
            'shift': get_shift_context(application.shift),
        }
    )


def create_message(application, owner, text):
    from apps.shifts.models import Message
    from .message import process_message_creation

    if text:
        message = Message.objects.create(
            application=application, owner=owner, text=text)
        process_message_creation(message, notify=False)

        return message

    return None


def process_approving(application, user, text):
    # TODO: send email to the resident about approving
    message = create_message(application, user, text)
    notify_application_state_changed(application, message)


def process_rejecting(application, user, text):
    # TODO: send email to the resident about postponing
    message = create_message(application, user, text)
    notify_application_state_changed(application, message)


def process_postponing(application):
    # TODO: send email to the resident about postponing
    message = create_message(
        application,
        application.shift.owner,
        "You application was postponed due to accepting an another application")
    notify_application_state_changed(application, message)


def process_renewing(application):
    # TODO: send email to application's owners about shift availability
    message = create_message(
        application,
        application.shift.owner,
        "The shift became available and your application was renewed")
    notify_application_state_changed(application, message)


def process_confirming(application, user, text):
    # TODO: send email to the scheduler about confirming
    message = create_message(application, user, text)
    notify_application_state_changed(application, message)


def process_cancelling(application, user, text):
    # TODO: send email to the other side about cancelling
    message = create_message(application, user, text)
    notify_application_state_changed(application, message)


def process_completing(application, user, text):
    # TODO: send email to the other side about completing
    message = create_message(application, user, text)
    notify_application_state_changed(application, message)
