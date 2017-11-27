from apps.accounts.notifications import notify_users


def notify_application_users(application, event, payload):
    notify_users([application.owner, application.shift.owner], event, payload)


def notify_about_application(application, event):
    from apps.shifts.serializers import ApplicationNotifySerializer

    notify_application_users(
        application,
        event,
        ApplicationNotifySerializer(application).data
    )


def notify_application_state_changed(application):
    notify_about_application(application, 'application_state_changed')


def notify_application_created(application):
    notify_about_application(application, 'application_created')


def notify_message_created(message):
    from apps.shifts.serializers import MessageNotifySerializer

    notify_application_users(
        message.application,
        'message_created',
        {'message': MessageNotifySerializer(message).data}
    )
