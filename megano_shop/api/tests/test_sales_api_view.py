from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests


class TestSalesAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__sales__get_request(self):
        a = [{'id': 1, 'price': 100.00, 'title': 'product title', 'href': '/product/1', 'images': [],
              'salePrice': 50.00, 'dateFrom': '20:00 16-04', 'dateTo': '20:00 21-04'}]

        url = reverse(f'api:sales')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, a)
