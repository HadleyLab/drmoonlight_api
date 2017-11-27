def process_shift_creation(shift):
    # TODO: send email to all suitable residents about new shift
    pass


def process_shift_updating(shift):
    if shift.has_active_applications:
        # TODO: send email to all active applicants about updated information
        active_applications = shift.applications.filter_active()

        pass
    else:
        # TODO: send email to all suitable residents about changing
        pass


def process_shift_deletion(shift):
    # TODO: send email to all applicants about the deletion
    pass
