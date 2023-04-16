import pytz
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from frontend.models import Order
from megano_shop.settings import TIME_ZONE
from users.models import Profile


class TestProfileAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__profile__get_request_without_auth_permission(self):
        url = reverse(f'api:profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__profile__get_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)

        profile = {'username': 'TestCase', 'first_name': 'Nikita', 'last_name': 'Orlov', 'email': 'test@test.ru',
                   'patronymic': 'Yurievich', 'phone': '+79999999999', 'avatar': {'src': None, 'alt': ''}}

        url = reverse(f'api:profile')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, profile)

    def test_api_route_named__account__get_request_without_auth_permission(self):
        url = reverse(f'api:account')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__account__get_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        created_1 = Order.objects.get(orderId=1).createdAt.astimezone(pytz.timezone(TIME_ZONE)).strftime(
            '%H:%M %d-%m-%Y')
        created_2 = Order.objects.get(orderId=2).createdAt.astimezone(pytz.timezone(TIME_ZONE)).strftime(
            '%H:%M %d-%m-%Y')
        account = {'username': 'TestCase', 'first_name': 'Nikita', 'last_name': 'Orlov', 'email': 'test@test.ru',
                   'patronymic': 'Yurievich', 'phone': '+79999999999', 'avatar': {'src': None, 'alt': ''},
                   'orders': [
                       {'user': 1, 'orderId': 1, 'createdAt': created_1, 'fullname': 'Orlov Nikita Yurievich',
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
                            'images': [], 'count_in_order': 10}]}]}

        url = reverse(f'api:account')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, account)

    def test_api_route_named__account__post_request_without_auth_permission(self):
        url = reverse(f'api:profile')
        data = {'last_name': 'Orlov', 'first_name': 'Nikita', 'patronymic': 'Yurievich',
                'phone': '+79653948778', 'email': 'o.orlow@ya.ru'}
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__profile__good_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:profile')
        data = [
            {'first_name': '', 'last_name': 'OrlovTest', 'email': 'o.orlow@ya.ru', 'patronymic': 'YurievichTest',
             'phone': '+79653948778'},
            {'first_name': 'NikitaTest', 'last_name': '', 'email': 'o.orlow@ya.ru', 'patronymic': 'YurievichTest',
             'phone': '+79653948778'},
            {'first_name': 'NikitaTest', 'last_name': 'OrlovTest', 'email': '', 'patronymic': 'YurievichTest',
             'phone': '+79653948778'},
        ]
        for i in data:
            response = self.client.post(url, data=i, format='json')
            user = User.objects.get(id=self.user.id)
            self.assertEqual(response.data, {**i, 'username': self.user.username})
            self.assertListEqual(
                [user.last_name, user.first_name, user.profile.patronymic, user.email, user.profile.phone],
                [i['last_name'], i['first_name'], i['patronymic'], i['email'], i['phone'], ]
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_route_named__profile__bad_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:profile')
        data = [
            {'last_name': 'Orlov', 'first_name': 'Nikita', 'patronymic': 'Yurievich', 'phone': '+796539487278',
             'email': 'o.orlow@ya.ru'},
            {'last_name': 'Orlov', 'first_name': 'Nikita', 'patronymic': '', 'phone': '+796539487278',
             'email': 'o.orlow@ya.ru'},
            {'last_name': 'Orlov', 'first_name': 'Nikita', 'patronymic': 'Yurievich', 'phone': '',
             'email': 'o.orlow@ya.ru'},
            {'last_name': 'Orlov', 'first_name': 'Nikita', 'patronymic': 'Yurievich', 'phone': '+79653948778',
             'email': 'o.orlow'},
        ]
        for i in data:
            response = self.client.post(url, data=i, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
