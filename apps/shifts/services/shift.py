from django.forms import model_to_dict

from apps.accounts.models import Resident
from apps.accounts.services.user import get_user_context
from apps.main.utils import async_send_mail


def get_shift_context(shift):
    return {
        'pk': shift.pk,
        'date_start': shift.date_start.strftime('%Y-%m-%d %H:%M'),
        'date_end': shift.date_end.strftime('%Y-%m-%d %H:%M'),
        'facility_name': shift.owner.facility_name,
        'department_name': shift.owner.department_name,
        'speciality_name': shift.speciality.name,
        'residency_years_required': shift.residency_years_required,
        'residency_program_name':
            shift.residency_program.name
            if shift.residency_program else None,
        'payment_amount': shift.payment_amount,
        'payment_per_hour': shift.payment_per_hour,
        'description': shift.description,
    }


def process_shift_creation(shift):
    suitable_residents = Resident.objects.filter_for_shift(shift) \
        .filter(notification_new_shifts=True)

    for resident in suitable_residents:
        async_send_mail('shift_created', resident.email, {
            'resident': get_user_context(resident),
            'shift': get_shift_context(shift),
        })


def process_shift_updating(shift):
    active_applications = shift.applications.filter_active()

    if active_applications.exists():
        suitable_residents = active_applications.all()
        is_applicant = True
    else:
        suitable_residents = Resident.objects.filter_for_shift(shift) \
            .filter(notification_new_shifts=True)
        is_applicant = False

    for resident in suitable_residents:
        async_send_mail('shift_updated', resident.email, {
            'resident': get_user_context(resident),
            'shift': get_shift_context(shift),
            'is_applicant': is_applicant,
        })


def process_shift_deletion(shift):
    active_applications = shift.applications.filter_active()

    if active_applications.exists():
        for resident in active_applications.all():
            async_send_mail('shift_deleted', resident.email, {
                'resident': get_user_context(resident),
                'shift': get_shift_context(shift),
            })
