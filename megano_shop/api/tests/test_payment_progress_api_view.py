from rest_framework import status
from rest_framework.reverse import reverse
from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD


class TestPaymentProgressAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__payment_progress__post_request_without_auth_permission(self):
        url = reverse(f'api:payment_progress')
        response = self.client.post(path=url, data={'payment_id': 100}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__payment_progress__good_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url_1 = reverse(f'api:payment')
        data = {'name': 'Orlov Nikita', 'number': '1233211323213222',
                'year': '2023', 'month': '10', 'code': '123',
                'order': 2, 'paid_for': 10500.0, 'user': self.user.id}

        response_1 = self.client.post(path=url_1, data=data, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        url_2 = reverse(f'api:payment_progress')
        response_2 = self.client.post(path=url_2, data=response_1.data, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response_2.data, 'Заказ успешно подтвержден и оплачен')

    def test_api_route_named__payment_progress__bad_post_request_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url_1 = reverse(f'api:payment')
        data = {'name': 'Orlov Nikita', 'number': '1233211323213221',
                'year': '2023', 'month': '10', 'code': '123',
                'order': 2, 'paid_for': 10500.0, 'user': self.user.id}

        response_1 = self.client.post(path=url_1, data=data, format='json')
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        url_2 = reverse(f'api:payment_progress')
        response_2 = self.client.post(path=url_2, data=response_1.data, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        errors = [
            'На карте недостаточно средств. Пожалуйста, попробуйте оплатить заказ другой картой',
            'При обработке платежа произошла ошибка',
            'Неправильно заполнены реквизиты банковской карты',
            'Счета с таким идентификатором не существует',
            'Оплата с использованием корпоративных карт запрещена. Необходимо использовать другую карту',
            'Превышено допустимое время оплаты по данному коду платежа',
        ]
        self.assertTrue(response_2.data in errors)
