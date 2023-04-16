from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD


class TestProfileSetPasswordAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__profile_password__post_request_without_auth_permission(self):
        url = reverse(f'api:profile_password')
        data = {'passwordCurrent': '', 'passwordNew': ''}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__profile_password__good_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:profile_password')
        data = {'passwordCurrent': TEST_PASSWORD, 'passwordNew': 'NewPass'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.data, {'message': 'Пароль успешно изменен'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_route_named__profile_password__bad_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:profile_password')
        data = {'passwordCurrent': 'WrongPass', 'passwordNew': 'NewPass'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.data, 'Неправильный текущий пароль!')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
