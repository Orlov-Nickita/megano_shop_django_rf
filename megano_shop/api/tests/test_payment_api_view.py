from rest_framework import status
from rest_framework.reverse import reverse
from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from frontend.models import Payment


class TestPaymentAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__payment__post_request_without_auth_permission(self):
        url = reverse(f'api:payment')
        data = {'name': 'Orlov Nikita', 'number': '1233211323213222',
                'year': '2023', 'month': '10', 'code': '123',
                'order': 2, 'paid_for': 10500.0, 'user': self.user.id}

        before = len(Payment.objects.all())
        response = self.client.post(path=url, data=data, format='json')
        after = len(Payment.objects.all())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(before, after)

    def test_api_route_named__payment__bad_post_request_with_auth_permission(self):
        url = reverse(f'api:payment')
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        data = [
            {'name': 'Orlov Nikita', 'number': '1233211323213222', 'year': '2000', 'month': '10', 'code': '123',
             'order': 2, 'paid_for': 10500.0, 'user': self.user.id},
            {'name': 'Orlov Nikita', 'number': '1233211323213222', 'year': '2030', 'month': '10', 'code': '123',
             'order': 2, 'paid_for': 10500.0, 'user': self.user.id},
            {'name': 'Orlov Nikita', 'number': '1233211323213222', 'year': '2023', 'month': '100', 'code': '123',
             'order': 2, 'paid_for': 10500.0, 'user': self.user.id},
            {'name': 'Orlov Nikita', 'number': '1233211323213222', 'year': '2023', 'month': '0', 'code': '123',
             'order': 2, 'paid_for': 10500.0, 'user': self.user.id},
            {'name': 'Orlov Nikita', 'number': '1233211323213222', 'year': '2023', 'month': '-10', 'code': '123',
             'order': 2, 'paid_for': 10500.0, 'user': self.user.id}
        ]

        for i in data:
            before = len(Payment.objects.all())
            response = self.client.post(path=url, data=i, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotEqual(response.data, {'payment_id': before + 1})
            self.assertEqual(response.data, 'Неверно указан год или месяц')

    def test_api_route_named__payment__good_post_request_with_auth_permission(self):
        url = reverse(f'api:payment')
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        data = {'name': 'Orlov Nikita', 'number': '1233211323213222', 'year': '2023', 'month': '10', 'code': '123',
                'order': 2, 'paid_for': 10500.0, 'user': self.user.id}

        before = len(Payment.objects.all())
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'payment_id': before + 1})
