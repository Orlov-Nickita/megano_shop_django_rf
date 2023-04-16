import pytz
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests
from frontend.models import Product
from megano_shop.settings import TIME_ZONE


class TestProductAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__product_detail__get_request(self):
        created = Product.objects.get(id=1).date.astimezone(pytz.timezone(TIME_ZONE)).strftime(
            '%H:%M %d-%m-%Y')
        a = {'id': 1, 'category': 1, 'price': 100.0, 'count_in_stock': 10,
             'date': created, 'title': 'product title',
             'description': 'product description', 'fullDescription': 'product fullDescription', 'available': True,
             'freeDelivery': True, 'rating': 0.0, 'href': '/product/1', 'specifications': [], 'reviews': [],
             'images': [], 'tags': []}

        url = reverse('api:product_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, a)
