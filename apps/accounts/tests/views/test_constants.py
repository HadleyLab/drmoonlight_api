from apps.accounts.factories import SpecialityFactory
from apps.accounts.models import TIMEZONES, US_STATES
from apps.main.tests import APITestCase


class ConstantsViewTestCase(APITestCase):
    def setUp(self):
        self.speciality = SpecialityFactory.create()

    def test_get_constants_by_unauthenticated_success(self):
        resp = self.client.get('/api/constants/')
        self.assertSuccessResponse(resp)

        self.assertDictEqual(
            resp.data, {
                'speciality': [{
                    'pk': self.speciality.pk,
                    'name': self.speciality.name,
                }],
                'timezones': [
                    {'pk': key, 'name': value} for key, value in TIMEZONES
                ],
                'us_states': [
                    {'pk': key, 'name': value} for key, value in US_STATES
                ],
            }
        )
