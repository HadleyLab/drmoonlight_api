from apps.accounts.services.user import get_user_context, localize_for_user
from apps.main.utils import async_send_mail
from apps.shifts.notifications import notify_application_state_changed
from .message import create_message
from .shift import get_shift_context


def get_opposite_side(application, user):
    """
    Returns opposite side for user
    """
    if user.is_resident:
        return application.shift.owner
    else:
        return application.owner


def get_application_context(application):
    return {
        'pk': application.pk,
    }


def get_context(application, comment=None):
    context = {
        'scheduler': get_user_context(application.shift.owner),
        'resident': get_user_context(application.owner),
        'application': get_application_context(application),
        'shift': get_shift_context(application.shift),
    }

    if comment:
        context.update({
            'comment': comment,
        })

    return context


def process_application(application, comment):
    create_message(application, application.owner, comment)

    with localize_for_user(application.shift.owner):
        async_send_mail(
            'application_created',
            application.shift.owner.email,
            get_context(application, comment)
        )


def process_invitation(application, comment):
    create_message(application, application.shift.owner, comment)

    with localize_for_user(application.owner):
        async_send_mail(
            'invitation_created',
            application.owner.email,
            get_context(application, comment)
        )


def process_state_changing(
        application, user, description, comment=''):
    """
    Creates new message for the application and notifies about state changing
    """
    if description and comment:
        text = '\n'.join([comment, description])
    else:
        text = ''.join([comment, description])

    message = create_message(application, user, text)

    notify_application_state_changed(application, message)


def process_approving(application, user, comment):
    process_state_changing(
        application,
        user,
        'The application is approved. Please, confirm that you will '
        'work on the shift',
        comment
    )

    with localize_for_user(application.owner):
        if application.owner.notification_application_status_changing:
            async_send_mail(
                'application_approved',
                application.owner.email,
                get_context(application, comment)
            )


def process_rejecting(application, user, comment):
    process_state_changing(
        application,
        user,
        'Your application is rejected. You may apply for other shifts '
        'at any time',
        comment)

    if application.owner.notification_application_status_changing:
        with localize_for_user(application.owner):
            async_send_mail(
                'application_rejected',
                application.owner.email,
                get_context(application)
            )


def process_postponing(application):
    process_state_changing(
        application,
        application.shift.owner,
        'You application is postponed due to accepting an another application'
    )

    if application.owner.notification_application_status_changing:
        with localize_for_user(application.owner):
            async_send_mail(
                'application_postponed',
                application.owner.email,
                get_context(application)
            )


def process_renewing(application):
    process_state_changing(
        application,
        application.shift.owner,
        'The shift became available and your application is renewed'
    )

    if application.owner.notification_application_status_changing:
        with localize_for_user(application.owner):
            async_send_mail(
                'application_renewed',
                application.owner.email,
                get_context(application)
            )


def process_confirming(application, user, comment):
    process_state_changing(
        application,
        user,
        'The application is confirmed',
        comment)

    with localize_for_user(application.shift.owner):
        async_send_mail(
            'application_confirmed',
            application.shift.owner.email,
            get_context(application, comment)
        )


def process_cancelling(application, user, comment):
    process_state_changing(
        application,
        user,
        'The application is cancelled',
        comment)

    destination = get_opposite_side(application, user)

    mail_notification_enabled = destination.is_scheduler or (
            destination.is_resident and
            destination.notification_application_status_changing
        )

    if mail_notification_enabled:
        with localize_for_user(destination):
            async_send_mail(
                'application_cancelled',
                destination.email,
                {
                    'source': get_user_context(user),
                    'destination': get_user_context(destination),
                    'comment': comment,
                    'application': get_application_context(application),
                    'shift': get_shift_context(application.shift),
                }
            )


def process_completing(application, user, comment):
    process_state_changing(
        application,
        user,
        'The application is completed',
        comment)

    if application.owner.notification_application_status_changing:
        with localize_for_user(application.owner):
            async_send_mail(
                'application_completed',
                application.owner.email,
                get_context(application, comment)
            )
