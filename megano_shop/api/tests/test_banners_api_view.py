from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests


class TestBannersAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__banners__get_request(self):
        a = [{'id': 1, 'price': 100, 'title': "product title", 'href': '/product/1', 'images': []},
             {'id': 2, 'price': 1000, 'title': "product title 2", 'href': '/product/2', 'images': []}]

        url = reverse(f'api:banners')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(response.data, a)
