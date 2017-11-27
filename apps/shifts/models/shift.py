from django.db import models
from django.db.models import Q
from django.utils import timezone

from contrib.easymoney import MoneyField

from apps.accounts.models import Scheduler, Speciality, ResidencyProgram
from apps.main.models import TimestampModelMixin


class ShiftStateEnum(object):
    COMPLETED = 'completed'
    WITHOUT_APPLIES = 'without_applies'
    COVERAGE_COMPLETED = 'coverage_completed'
    REQUIRE_APPROVAL = 'require_approval'


class ShiftQuerySet(models.QuerySet):
    def filter_for_resident(self, resident):
        if resident.is_approved:
            # An approved resident can see only suitable shifts for him
            return self.filter(
                Q(residency_program=resident.residency_program) |
                Q(residency_program__isnull=True),
                speciality__in=resident.specialities.all(),
                residency_years_required__lte=resident.residency_years
            )

        # A not approved resident can see all shifts (but cannot apply for them)
        return self

    def filter_for_scheduler(self, scheduler):
        return self.filter(owner=scheduler)

    def filter_for_user(self, user):
        if user.is_scheduler:
            return self.filter_for_scheduler(user.scheduler)

        if user.is_resident:
            return self.filter_for_resident(user.resident)

        return self.none()  # pragma: no cover


class Shift(TimestampModelMixin, models.Model):
    # TODO: Improve future dates support (with DST)
    date_start = models.DateTimeField(
        verbose_name='Date start'
    )
    date_end = models.DateTimeField(
        verbose_name='Date end'
    )
    owner = models.ForeignKey(
        Scheduler,
        related_name='shifts',
        verbose_name='Owner'
    )
    speciality = models.ForeignKey(
        Speciality,
        verbose_name='Speciality'
    )
    residency_program = models.ForeignKey(
        ResidencyProgram,
        verbose_name='Residency program',
        null=True, blank=True
    )
    residency_years_required = models.PositiveIntegerField(
        verbose_name='Residency years required',
        default=0
    )
    payment_amount = MoneyField(
        verbose_name='Payment amount'
    )
    payment_per_hour = models.BooleanField(
        verbose_name='Payment per hour'
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True
    )

    objects = ShiftQuerySet.as_manager()

    class Meta:
        verbose_name = 'Shift'
        verbose_name_plural = 'Shifts'

    def __str__(self):
        return "For {0} from {1} to {2}".format(
            self.speciality,
            self.date_start.strftime('%Y-%m-%d %H:%M'),
            self.date_end.strftime('%Y-%m-%d %H:%M'))

    @property
    def is_started(self):
        return self.date_start <= timezone.now()

    @property
    def is_ended(self):
        return self.date_end < timezone.now()

    @property
    def state(self):
        from .application import ApplicationStateEnum

        if self.is_ended:
            # TODO: think about checking applications in the COMPLETED state
            # TODO: may be failed applications shouldn't make a shift completed
            # TODO: but now I think, there is no reasons not to consider
            # TODO: the ended shift as completed
            return ShiftStateEnum.COMPLETED

        applications_count = self.applications.aggregate_count_by_state()

        confirmed = applications_count.get(ApplicationStateEnum.CONFIRMED, 0)
        approved = applications_count.get(ApplicationStateEnum.APPROVED, 0)
        if confirmed or approved:
            return ShiftStateEnum.COVERAGE_COMPLETED

        new = applications_count.get(ApplicationStateEnum.NEW, 0)
        if new:
            return ShiftStateEnum.REQUIRE_APPROVAL

        return ShiftStateEnum.WITHOUT_APPLIES

    @property
    def is_coverage_completed(self):
        return self.state == ShiftStateEnum.COVERAGE_COMPLETED

    @property
    def has_active_applications(self):
        return self.state in [
            ShiftStateEnum.COVERAGE_COMPLETED,
            ShiftStateEnum.REQUIRE_APPROVAL,
        ]
