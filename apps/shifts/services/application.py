def process_application(application):
    # TODO: send email to the shift's scheduler about new application
    pass


def process_invitation(application):
    # TODO: send email to the resident about invitation
    pass


def create_message(application, user, message):
    from apps.shifts.models import Message
    from .message import process_message_creation

    message = Message.objects.create(
        application=application, owner=user, message=message)
    process_message_creation(message)

    return message


def process_approving(application, user, message):
    # TODO: send email to the resident about approving
    create_message(application, user, message)


def process_rejecting(application, user, message):
    # TODO: send email to the resident about postponing
    create_message(application, user, message)


def process_postponing(application):
    # TODO: send email to the resident about postponing
    create_message(
        application,
        application.shift.owner,
        "You application was postponed due to accepting an another application")


def process_renewing(application):
    # TODO: send email to application's owners about shift availability
    create_message(
        application,
        application.shift.owner,
        "The shift became available and your application was renewed")


def process_confirming(application, user, message):
    # TODO: send email to the scheduler about confirming
    create_message(application, user, message)


def process_cancelling(application, user, message):
    # TODO: send email to the other side about cancelling
    create_message(application, user, message)


def process_completing(application, user, message):
    # TODO: send email to the other side about completing
    create_message(application, user, message)
