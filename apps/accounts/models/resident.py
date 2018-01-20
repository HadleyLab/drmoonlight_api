from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_fsm import FSMIntegerField, transition

from apps.accounts.services.resident import process_resident_approving, \
    process_resident_rejecting, process_resident_profile_filling
from .choices import US_STATES
from .user import User, UserManager
from .speciality import Speciality


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
    state_license_states = ArrayField(
        models.CharField(max_length=2, choices=US_STATES),
        verbose_name='State licence\'s states',
        blank=True, null=True
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
    REJECTED = 4

    CHOICES = (
        (NEW, 'New'),
        (PROFILE_FILLED, 'Profile filled'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )


def is_account_manager(instance, user):
    return user.is_account_manager


def is_resident(instance, user):
    return user.is_resident and instance.user_ptr == user


class ResidentQuerySet(models.QuerySet):
    def filter_for_shift(self, shift):
        """
        Returns suitable approved residents
        """
        filter_kwargs = {
            'residency_years__gte': shift.residency_years_required,
            'specialities': shift.speciality,
        }

        return self.filter_approved().filter(
            **filter_kwargs
        )

    def filter_approved(self):
        return self.filter(state=ResidentStateEnum.APPROVED)


class ResidentManager(models.Manager.from_queryset(ResidentQuerySet),
                      UserManager):
    pass


class Resident(ResidentNotificationSettingsMixin,
               ResidentProfileSettingsMixin, User):
    specialities = models.ManyToManyField(
        Speciality,
        verbose_name='Specialities',
        related_name='residents',
        blank=True
    )
    residency_program = models.TextField(
        verbose_name='Residency program',
        null=True, blank=True
    )
    residency_years = models.PositiveIntegerField(
        verbose_name='Residency years',
        null=True, blank=True
    )
    state = FSMIntegerField(
        verbose_name='State',
        default=ResidentStateEnum.NEW,
        choices=ResidentStateEnum.CHOICES
    )

    objects = ResidentManager()

    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'

    @property
    def is_approved(self):
        return self.state == ResidentStateEnum.APPROVED

    @transition(
        field=state,
        source=[ResidentStateEnum.NEW, ResidentStateEnum.REJECTED],
        target=ResidentStateEnum.PROFILE_FILLED,
        permission=is_resident
    )
    def fill_profile(self, profile_data):
        for field, value in profile_data.items():
            setattr(self, field, value)

        process_resident_profile_filling(self)

    @transition(
        field=state,
        source=ResidentStateEnum.PROFILE_FILLED,
        target=ResidentStateEnum.APPROVED,
        permission=is_account_manager
    )
    def approve(self):
        process_resident_approving(self)

    @transition(
        field=state,
        source=ResidentStateEnum.PROFILE_FILLED,
        target=ResidentStateEnum.REJECTED,
        permission=is_account_manager
    )
    def reject(self):
        process_resident_rejecting(self)
