import os
import re

from django.conf import settings

from apps.accounts.factories import SchedulerFactory
from apps.accounts.models import Scheduler
from apps.main.tests import APITestCase


class SchedulerViewSetTestCase(APITestCase):
    def test_create_token_as_scheduler(self):
        token = self.create_token(self.scheduler)
        self.assertIsNotNone(token)

    def test_create_token_as_not_active_scheduler(self):
        scheduler = SchedulerFactory.create(is_active=False)
        token = self.create_token(scheduler)
        self.assertIsNone(token)

    def test_create(self):
        data = {
            'email': 'scheduler@gmail.com',
            'password': 'Str0ngPassW0RD',
            'department_name': 'Department',
            'facility_name': 'Facility',
            'first_name': 'First',
            'last_name': 'Last',
        }
        resp = self.client.post('/api/accounts/scheduler/', data)
        self.assertSuccessResponse(resp)

        scheduler = Scheduler.objects.get(pk=resp.data['pk'])
        self.assertFalse(scheduler.is_active)
        self.assertEqual(scheduler.email, data['email'])
        self.assertEqual(scheduler.first_name, data['first_name'])
        self.assertEqual(scheduler.last_name, data['last_name'])
        self.assertEqual(scheduler.department_name, data['department_name'])
        self.assertEqual(scheduler.facility_name, data['facility_name'])
        self.assertTrue(scheduler.check_password(data['password']))

    def test_create_without_first_and_last_name_failed(self):
        data = {
            'email': 'scheduler@gmail.com',
            'password': 'Str0ngPassW0RD',
            'department_name': 'Department',
            'facility_name': 'Facility',
            'first_name': '',
            'last_name': '',
        }
        resp = self.client.post('/api/accounts/scheduler/', data)
        self.assertBadRequest(resp)

    def test_retrieve_by_unauthenticated_failed(self):
        resp = self.client.get('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertForbidden(resp)

    def test_retrieve_myself_by_scheduler_success(self):
        self.authenticate_as_scheduler()
        resp = self.client.get('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertSuccessResponse(resp)

    def test_retrieve_not_myself_by_scheduler_failed(self):
        scheduler = SchedulerFactory.create()
        self.authenticate_as_scheduler(scheduler)
        resp = self.client.get('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertForbidden(resp)

    def test_retrieve_by_resident_failed(self):
        self.authenticate_as_resident()
        resp = self.client.get('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertForbidden(resp)

    def test_retrieve_by_account_manager_success(self):
        self.authenticate_as_account_manager()
        resp = self.client.get('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertSuccessResponse(resp)

    def test_update_by_account_manager_failed(self):
        self.authenticate_as_account_manager()
        resp = self.client.patch('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertForbidden(resp)

    def test_update_by_resident_failed(self):
        self.authenticate_as_resident()
        resp = self.client.patch('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertForbidden(resp)

    def test_update_not_self_by_scheduler_failed(self):
        scheduler = SchedulerFactory.create()
        self.authenticate_as_scheduler(scheduler)
        resp = self.client.patch('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk))
        self.assertForbidden(resp)

    def test_update_myself_by_scheduler_success(self):
        self.authenticate_as_scheduler()
        data = {
            'department_name': 'Another department',
            'facility_name': 'Another facility',
        }
        resp = self.client.patch('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk), data, format='json')
        self.assertSuccessResponse(resp)

        self.scheduler.refresh_from_db()
        self.assertEqual(
            self.scheduler.department_name, data['department_name'])
        self.assertEqual(self.scheduler.facility_name, data['facility_name'])

    def test_update_avatar(self):
        self.authenticate_as_scheduler()
        self.assertFalse(self.scheduler.avatar)

        avatar_path = os.path.join(
            settings.BASE_DIR, 'apps/accounts/tests/fixtures/', 'avatar.jpg')
        data = {
            'avatar': open(avatar_path, 'rb')
        }
        resp = self.client.patch('/api/accounts/scheduler/{0}/'.format(
            self.scheduler.pk), data, format='multipart')
        self.assertSuccessResponse(resp)
        self.assertIsNotNone(
            re.findall('/media/avatars/Scheduler/{0}'.format(self.scheduler.pk),
                       resp.data['avatar']))

        self.scheduler.refresh_from_db()
        self.assertTrue(self.scheduler.avatar)
