from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests


class TestTagsAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__tags__get_request(self):
        a = [{'id': 'tag_1_id', 'name': 'tag_1_name'},
             {'id': 'tag_2_id', 'name': 'tag_2_name'}]
        url = reverse(f'api:tags')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, a)
