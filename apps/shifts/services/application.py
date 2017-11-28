from apps.shifts.notifications import notify_application_state_changed


def process_application(application):
    # TODO: send email to the shift's scheduler about new application
    pass


def process_invitation(application):
    # TODO: send email to the resident about invitation
    pass


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
