from apps.shifts.notifications import notify_message_created


def process_message_creation(message):
    # TODO: send email to the opposite side
    notify_message_created(message)
