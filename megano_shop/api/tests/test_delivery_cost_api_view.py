from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests
from frontend.models import Order


class TestDeliveryCostAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__deliveryCost__get_request(self):
        order = Order.objects.get(orderId=1)
        url = reverse('api:deliveryCost',
                      kwargs={'total_cost': int(order.totalCost), 'delivery_type': order.deliveryType})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 0)
