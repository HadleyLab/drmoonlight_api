from apps.main.tests import APITestCase


class MeViewTestCase(APITestCase):
    def test_get_failed_for_unauthorized(self):
        resp = self.client.get('/api/accounts/me/')
        self.assertForbidden(resp)

    def test_get_success_for_resident(self):
        self.authenticate_as_resident()
        resp = self.client.get('/api/accounts/me/')
        self.assertSuccessResponse(resp)

        self.assertEqual(resp.data['pk'], self.resident.pk)
        self.assertTrue(resp.data['is_resident'])
        self.assertFalse(resp.data['is_scheduler'])
        self.assertFalse(resp.data['is_account_manager'])

    def test_get_success_for_scheduler(self):
        self.authenticate_as_scheduler()
        resp = self.client.get('/api/accounts/me/')
        self.assertSuccessResponse(resp)

        self.assertEqual(resp.data['pk'], self.scheduler.pk)
        self.assertFalse(resp.data['is_resident'])
        self.assertTrue(resp.data['is_scheduler'])
        self.assertFalse(resp.data['is_account_manager'])

    def test_get_success_for_account_manager(self):
        self.authenticate_as_account_manager()
        resp = self.client.get('/api/accounts/me/')
        self.assertSuccessResponse(resp)

        self.assertEqual(resp.data['pk'], self.account_manager.pk)
        self.assertFalse(resp.data['is_resident'])
        self.assertFalse(resp.data['is_scheduler'])
        self.assertTrue(resp.data['is_account_manager'])
