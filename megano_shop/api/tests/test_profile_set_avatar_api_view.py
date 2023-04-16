import os.path
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from megano_shop.settings import MEDIA_ROOT, BASE_DIR


class TestProfileSetAvatarAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__profile_avatar__post_request_without_auth_permission(self):
        url = reverse(f'api:profile_avatar')
        data = 'File'
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__profile_avatar__good_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:profile_avatar')

        with open(f'{MEDIA_ROOT}avatars/me.jpg', 'rb') as file:
            filename = os.path.basename(file.name)
            headers = {'HTTP_CONTENT_DISPOSITION': f'form-data; filename={filename}'}
            data = {'file': SimpleUploadedFile(name=f'{filename}', content=file.read(), content_type='image/jpeg')}

            response = self.client.post(path=url, data=data, format='multipart', **headers)
            file_path = os.path.exists(f'{BASE_DIR}{response.data["src"]}')
            self.assertTrue(file_path)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            if file_path:
                os.remove(f'{BASE_DIR}{response.data["src"]}')
