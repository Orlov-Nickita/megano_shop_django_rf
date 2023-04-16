from http.cookies import SimpleCookie

import pytz
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from frontend.models import Order
from megano_shop.settings import TIME_ZONE


class TestOrderActiveAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__orders_active__get_request_without_auth_permission(self):
        url = reverse(f'api:orders_active')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__orders_active__get_request_without_cookie_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        active_order = Order.objects.filter(user_id=self.user.id,
                                            status=Order.StatusChoice.NOT_ACCEPTED).first()
        url = reverse(f'api:orders_active')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if not active_order:
            self.assertEqual(response.data, 'Активного заказа нет')
        else:
            created = Order.objects.get(orderId=2).createdAt.astimezone(
                pytz.timezone(TIME_ZONE)).strftime('%H:%M %d-%m-%Y')
            order = {'user': 1, 'orderId': 2, 'createdAt': created, 'fullname': 'Orlov Nikita Yurievich',
                     'email': 'test@test.ru', 'phone': '+79999999999', 'deliveryType': 'Обычная',
                     'paymentType': 'Онлайн картой', 'totalCost': 10500.0, 'deliveryCost': 200.0,
                     'status': 'Заказ не оплачен', 'city': 'Moscow', 'address': 'Russia', 'freeDelivery': False,
                     'products': [
                         {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': [],
                          'count_in_order': 5},
                         {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': [],
                          'count_in_order': 10}]}
            self.assertEqual(response.data, order)

    def test_api_route_named__orders_active__get_request_with_cookie_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:orders_active')
        order = Order.objects.create(
            user=self.user,
            orderId=22,
            totalCost=100,
        )
        self.client.cookies.load({
            'order_id_from_history': 22
        })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(order.orderId, response.data['orderId'])
