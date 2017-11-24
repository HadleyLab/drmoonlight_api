from apps.accounts.factories import ResidencyProgramFactory, SpecialityFactory
from apps.main.tests import APITestCase


class ConstantsViewTestCase(APITestCase):
    def setUp(self):
        self.residency_program = ResidencyProgramFactory.create()
        self.speciality = SpecialityFactory.create()

    def test_get_constants_by_unauthenticated_success(self):
        resp = self.client.get('/api/constants/')
        self.assertSuccessResponse(resp)

        self.assertDictEqual(
            resp.data, {
                'residency_program': [{
                    'pk': self.residency_program.pk,
                    'name': self.residency_program.name,
                }],
                'speciality': [{
                    'pk': self.speciality.pk,
                    'name': self.speciality.name,
                }],
            }
        )
