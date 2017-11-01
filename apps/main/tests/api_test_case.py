from rest_framework.test import APITestCase as BaseAPITestCase
from rest_framework import status

from apps.accounts.factories import SchedulerFactory, ResidentFactory


class APITestCase(BaseAPITestCase):
    def setUp(self):
        super(APITestCase, self).setUp()

        self.scheduler = SchedulerFactory(password='password')
        self.resident = ResidentFactory(password='password')

    def assertSuccessResponse(self, resp):
        if resp.status_code not in range(200, 300):
            raise self.failureException(
                'Response status is not success. Status code: {0}\n'
                'Response data is:\n{1}'.format(resp.status_code, resp.data))

    def assertNotAllowed(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def assertBadRequest(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def assertUnauthorized(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertForbidden(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotFound(self, resp):
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def create_token(self, user=None):
        resp = self.client.post('/api/accounts/token/create/', {
            'email': user.email,
            'password': 'password',
        })

        if resp.status_code == status.HTTP_200_OK:
            return resp.data['auth_token']

        return None

    def authenticate_as_scheduler(self, scheduler=None):
        if scheduler is None:
            scheduler = self.scheduler
        token = self.create_token(scheduler)
        self.assertIsNotNone(token)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )

    def authenticate_as_resident(self, resident=None):
        if resident is None:
            resident = self.resident
        token = self.create_token(resident)
        self.assertIsNotNone(token)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token {0}'.format(token)
        )
