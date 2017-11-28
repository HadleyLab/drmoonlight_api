from apps.accounts.notifications import notify_user
from apps.main.serializers.utils import get_request_user_context


def notify_application_state_changed(application, message=None):
    def get_payload_fn(context):
        from apps.shifts.serializers import (
            ApplicationSerializer, MessageSerializer)

        return lambda: {
            'application': ApplicationSerializer(
                application, context=context).data,
            'message':
                MessageSerializer(message, context=context).data
                if message else None,
        }

    for user in [application.owner, application.shift.owner]:
        notify_user(
            user,
            'application_state_changed',
            get_payload_fn(get_request_user_context(user))
        )


def notify_message_created(message):
    application = message.application

    def get_payload_fn(context):
        from apps.shifts.serializers import MessageSerializer

        return lambda: {
            'message': MessageSerializer(message, context=context).data,
        }

    for user in [application.owner, application.shift.owner]:
        notify_user(
            user,
            'message_created',
            get_payload_fn(get_request_user_context(user))
        )
