from django.db import models
from django_fsm import FSMIntegerField, transition

from .user import User
from .speciality import Speciality
from .residency_program import ResidencyProgram


class ResidentProfileSettingsMixin(models.Model):
    earliest_availability_for_shift = models.TextField(
        verbose_name='Earliest availability for a shift',
        blank=True
    )
    preferences_for_work_location = models.TextField(
        verbose_name='Preferences for a work location',
        blank=True
    )
    state_license = models.BooleanField(
        verbose_name='Has state licence',
        default=False
    )
    state = models.CharField(
        verbose_name='State licence\'s state',
        max_length=255,
        blank=True
    )
    federal_dea_active = models.BooleanField(
        verbose_name='Is federal dea active',
        default=False
    )
    bls_acls_pals = models.NullBooleanField(
        verbose_name='Has BLC/ACLS/PALS',
        default=None
    )
    active_permanent_residence_card_or_visa = models.NullBooleanField(
        verbose_name='Has active permanent residence card or visa',
        default=None
    )
    active_current_driver_license_or_passport = models.BooleanField(
        verbose_name='Has active current driver license or passport',
        default=False
    )
    active_npi_number = models.BooleanField(
        verbose_name='Has active npi number',
        default=False
    )
    ecfmg = models.NullBooleanField(
        verbose_name='ECFMG',
        default=None
    )
    active_board_certificates = models.NullBooleanField(
        verbose_name='Has active board certificates',
        default=None
    )

    class Meta:
        abstract = True


class ResidentNotificationSettingsMixin(models.Model):
    notification_new_shifts = models.BooleanField(
        verbose_name='Notify about new shifts',
        default=True
    )
    notification_application_status_changing = models.BooleanField(
        verbose_name='Notify about an application status changing',
        default=True
    )
    notification_new_messages = models.BooleanField(
        verbose_name='Notify about new messages',
        default=True
    )

    class Meta:
        abstract = True


class ResidentStateEnum(object):
    NEW = 1
    PROFILE_FILLED = 2
    APPROVED = 3


class Resident(ResidentNotificationSettingsMixin,
               ResidentProfileSettingsMixin, User):
    specialities = models.ManyToManyField(
        Speciality,
        verbose_name='Specialities',
        blank=True
    )
    residency_program = models.ForeignKey(
        ResidencyProgram,
        verbose_name='Residency program',
        null=True, blank=True
    )
    residency_year = models.PositiveIntegerField(
        verbose_name='Residency year',
        null=True, blank=True
    )
    state = FSMIntegerField(
        verbose_name='State',
        default=ResidentStateEnum.NEW
    )

    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'

    @transition(
        field=state,
        source=ResidentStateEnum.NEW,
        target=ResidentStateEnum.PROFILE_FILLED
    )
    def fill_profile(self):
        # TODO: send email to the managing editor
        pass

    @transition(
        field=state,
        source=ResidentStateEnum.PROFILE_FILLED,
        target=ResidentStateEnum.APPROVED
        # TODO: only account manager
    )
    def approve(self):
        # TODO: send email to the resident
        pass
