from apps.accounts.notifications import notify_user
from apps.main.serializers.utils import get_request_user_context


def notify_application_state_changed(application, message=None):
    from apps.shifts.serializers import (
        ApplicationSerializer, MessageSerializer)

    for user in [application.owner, application.shift.owner]:
        context = get_request_user_context(user)

        notify_user(
            user,
            'application_state_changed',
            lambda: {
                'application': ApplicationSerializer(
                    application, context=context).data,
                'message':
                    MessageSerializer(message, context=context).data
                    if message else None,
            }
        )


def notify_message_created(message):
    from apps.shifts.serializers import MessageSerializer

    application = message.application

    for user in [application.owner, application.shift.owner]:
        context = get_request_user_context(user)

        notify_user(
            user,
            'message_created',
            lambda: {
                'message': MessageSerializer(message, context=context).data,
            }
        )
