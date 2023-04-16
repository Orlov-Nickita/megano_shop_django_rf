import pytz
from rest_framework import status
from rest_framework.reverse import reverse

from api.serializers import BasketProductsSerializer, BasketSerializer
from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from frontend.models import Order, Basket, BasketProducts, OrderProducts
from megano_shop.settings import TIME_ZONE


class TestOrdersAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__orders_detail__get_request_without_auth_permission(self):
        url = reverse(f'api:orders_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__orders_detail__get_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)

        created = Order.objects.get(orderId=1).createdAt.astimezone(pytz.timezone(TIME_ZONE)).strftime('%H:%M %d-%m-%Y')
        order = {'user': 1, 'orderId': 1, 'createdAt': created,
                 'fullname': 'Orlov Nikita Yurievich', 'email': 'test@test.ru', 'phone': '+79999999999',
                 'deliveryType': 'Обычная', 'paymentType': 'Онлайн картой', 'totalCost': 10500.0,
                 'deliveryCost': 200.0, 'status': 'Заказ оплачен', 'city': 'Moscow', 'address': 'Russia',
                 'freeDelivery': False,
                 'products': [
                     {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': [],
                      'count_in_order': 5},
                     {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': [],
                      'count_in_order': 10}]}

        url = reverse('api:orders_detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, order)

    def test_api_route_named__orders__get_request_without_auth_permission(self):
        url = reverse(f'api:orders')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__orders__get_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        created_1 = Order.objects.get(orderId=1).createdAt.astimezone(pytz.timezone(TIME_ZONE)).strftime(
            '%H:%M %d-%m-%Y')
        created_2 = Order.objects.get(orderId=2).createdAt.astimezone(pytz.timezone(TIME_ZONE)).strftime(
            '%H:%M %d-%m-%Y')
        orders = [{'user': 1, 'orderId': 1, 'createdAt': created_1, 'fullname': 'Orlov Nikita Yurievich',
                   'email': 'test@test.ru', 'phone': '+79999999999', 'deliveryType': 'Обычная',
                   'paymentType': 'Онлайн картой', 'totalCost': 10500.0, 'deliveryCost': 200.0,
                   'status': 'Заказ оплачен', 'city': 'Moscow', 'address': 'Russia', 'freeDelivery': False,
                   'products': [{'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1',
                                 'images': [], 'count_in_order': 5},
                                {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2',
                                 'images': [], 'count_in_order': 10}]},
                  {'user': 1, 'orderId': 2, 'createdAt': created_2, 'fullname': 'Orlov Nikita Yurievich',
                   'email': 'test@test.ru', 'phone': '+79999999999', 'deliveryType': 'Обычная',
                   'paymentType': 'Онлайн картой', 'totalCost': 10500.0, 'deliveryCost': 200.0,
                   'status': 'Заказ не оплачен', 'city': 'Moscow', 'address': 'Russia',
                   'freeDelivery': False, 'products': [
                      {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1',
                       'images': [], 'count_in_order': 5},
                      {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2',
                       'images': [], 'count_in_order': 10}]}]

        url = reverse('api:orders')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, orders)

    def test_api_route_named__orders__post_request_without_auth_permission(self):
        url = reverse(f'api:orders')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__orders__post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:orders')
        basket = Basket.objects.filter(user_id=self.user.id)
        data = {
            'basketId': basket.get().id
        }
        basket_products = list(basket.get().basketproducts_set.values('product_id', 'count_in_basket'))

        self.assertEqual(len(basket), 1)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        basket = Basket.objects.filter(user_id=self.user.id)
        self.assertFalse(basket)
        self.assertEqual(len(basket), 0)
        order = Order.objects.get(orderId=response.data['id'])
        order_products = list(order.orderproducts_set.values('product_id', 'count_in_order'))
        self.assertTrue(order)
        self.assertEqual(len(basket_products), len(order_products))
        for i in range(len(basket_products)):
            self.assertEqual(basket_products[i]['product_id'], order_products[i]['product_id'])
            self.assertEqual(basket_products[i]['count_in_basket'], order_products[i]['count_in_order'])

    def test_api_route_named__orders_detail__post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        pk = 2
        url = reverse(f'api:orders_detail', kwargs={'pk': pk})

        created = Order.objects.get(orderId=pk).createdAt.astimezone(pytz.timezone(TIME_ZONE)).strftime(
            '%H:%M %d-%m-%Y')
        before_order = {'user': self.user.id, 'orderId': pk, 'createdAt': created, 'fullname': 'Orlov Nikita Yurievich',
                        'email': 'test@test.ru', 'phone': '+79999999999', 'deliveryType': 'Обычная',
                        'paymentType': 'Онлайн картой', 'totalCost': 10500.0, 'deliveryCost': 200.0,
                        'status': 'Заказ не оплачен', 'city': 'Moscow', 'address': 'Russia', 'freeDelivery': False,
                        'products': [
                            {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': [],
                             'count_in_order': 5},
                            {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': [],
                             'count_in_order': 10}]}

        response_get_before = self.client.get(url, format='json')
        self.assertEqual(before_order, response_get_before.data)

        after_order = {'user': self.user.id, 'orderId': pk, 'fullname': 'TEST TEST TEST',
                       'email': 'ORLOV@NIKITA.ru', 'phone': '+79653948778', 'deliveryType': 'Обычная',
                       'paymentType': 'Онлайн картой', 'totalCost': 10500.0, 'deliveryCost': 200.0,
                       'status': Order.StatusChoice.ACCEPTED,
                       'city': 'Piter', 'address': 'Russia Masha', 'freeDelivery': False,
                       'products': [
                           {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': [],
                            'count_in_order': 10},
                           {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': [],
                            'count_in_order': 20}]}

        response_post = self.client.post(url, data=after_order, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        response_get_after = self.client.get(url, format='json').data
        response_get_after.pop('createdAt')
        self.assertEqual(after_order, response_get_after)
