from django.test import TestCase, mock

from apps.accounts.factories import ResidentFactory
from apps.accounts.models import ResidentStateEnum
from apps.shifts.factories import ApplicationFactory, ShiftFactory
from apps.shifts.models import ApplicationStateEnum
from apps.shifts.services.shift import (
    process_shift_creation, process_shift_deletion, process_shift_updating)


class  ShiftServiceTestCase(TestCase):
    def setUp(self):
        self.resident = ResidentFactory.create()
        self.shift = ShiftFactory.create()
        self.application = ApplicationFactory.create(
            shift=self.shift, owner=self.resident)

    @mock.patch('apps.shifts.services.shift.async_send_mail', autospec=True)
    def test_process_shift_creation_works_correctly(
            self, mock_async_send_mail):
        # Not suitable resident
        ResidentFactory.create(
            state=ResidentStateEnum.APPROVED)
        # Suitable resident with notification disabled settings
        ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            specialities=[self.shift.speciality],
            residency_years=self.shift.residency_years_required,
            notification_new_shifts=False
        )
        suitable_resident = ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            specialities=[self.shift.speciality],
            residency_years=self.shift.residency_years_required)

        process_shift_creation(self.shift)

        mock_async_send_mail.assert_called_once()
        _, first_call_args, _ = mock_async_send_mail.mock_calls[0]
        self.assertEqual(first_call_args[1], suitable_resident.email)

    def test_process_shift_creation_works_without_errors(self):
        ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            specialities=[self.shift.speciality],
            residency_years=self.shift.residency_years_required)

        process_shift_creation(self.shift)

    @mock.patch('apps.shifts.services.shift.async_send_mail', autospec=True)
    def test_process_shift_updating_with_active_applicants_works_correctly(
            self, mock_async_send_mail):
        # Create suitable resident without application
        ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            specialities=[self.shift.speciality],
            residency_years=self.shift.residency_years_required)

        process_shift_updating(self.shift)

        mock_async_send_mail.assert_called_once()
        _, first_call_args, _ = mock_async_send_mail.mock_calls[0]
        self.assertEqual(first_call_args[1], self.resident.email)

    @mock.patch('apps.shifts.services.shift.async_send_mail', autospec=True)
    def test_process_shift_updating_without_active_applicants_works_correctly(
            self, mock_async_send_mail):
        self.application.state = ApplicationStateEnum.CANCELLED
        self.application.save()

        # Create suitable resident without application
        suitable_resident = ResidentFactory.create(
            state=ResidentStateEnum.APPROVED,
            specialities=[self.shift.speciality],
            residency_years=self.shift.residency_years_required)

        process_shift_updating(self.shift)

        mock_async_send_mail.assert_called_once()
        _, first_call_args, _ = mock_async_send_mail.mock_calls[0]
        self.assertEqual(first_call_args[1], suitable_resident.email)

    def test_process_shift_updating_works_without_errors(self):
        process_shift_updating(self.shift)

    @mock.patch('apps.shifts.services.shift.async_send_mail', autospec=True)
    def test_process_shift_deletion_without_active_applications_works_correctly(
         self, mock_async_send_mail):
        self.application.state = ApplicationStateEnum.CANCELLED
        self.application.save()
        
        process_shift_deletion(self.shift)
        
        mock_async_send_mail.assert_not_called()
        
    @mock.patch('apps.shifts.services.shift.async_send_mail', autospec=True)
    def test_process_shift_deletion_with_active_applications_works_correctly(
            self, mock_async_send_mail):
        process_shift_deletion(self.shift)
        
        mock_async_send_mail.assert_called_once()
        _, first_call_args, _ = mock_async_send_mail.mock_calls[0]
        self.assertEqual(first_call_args[1], self.resident.email)

    def test_process_shift_deletion_works_without_errors(self):
        process_shift_deletion(self.shift)
