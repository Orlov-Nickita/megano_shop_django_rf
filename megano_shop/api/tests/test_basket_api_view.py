from jinja2.lexer import TOKEN_DOT
from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from frontend.models import Basket


class TestBasketAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__basket__get_request_without_auth_permission(self):
        url = reverse(f'api:basket')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'auth_error': 'Пользователь не аутентифицирован'})

    def test_api_route_named__basket__get_request_with_auth_permission(self):
        a = [{'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': [],
              'count_in_basket': 5},
             {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': [],
              'count_in_basket': 10}]
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        url = reverse(f'api:basket')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['products'], a)

    def test_api_route_named__basket__post_request_without_auth_permission(self):
        url = reverse(f'api:basket')
        data = {
            'id': 1,
            'count': 2,
        }
        basket_count_before = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        response = self.client.post(path=url, data=data, format='json')

        basket_count_after = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        self.assertListEqual(
            [response.data, response.status_code, basket_count_before],
            [{'auth_error': 'Пользователь не аутентифицирован'}, status.HTTP_200_OK, basket_count_after]
        )

    def test_api_route_named__basket__post_request_with_auth_permission(self):
        url = reverse(f'api:basket')
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        data = {
            'id': 1,
            'count': 2,
        }
        basket_count_before = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        response = self.client.post(path=url, data=data, format='json')

        basket_count_after = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        self.assertListEqual(
            [response.status_code, response.data, basket_count_after],
            [status.HTTP_200_OK, data, basket_count_before + data['count']]
        )

    def test_api_route_named__basket__delete_request_without_auth_permission(self):
        url = reverse(f'api:basket')
        data = {
            'id': 1,
            'count': 2,
        }

        basket_count_before = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        response = self.client.delete(path=url, data=data, format='json')

        basket_count_after = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        self.assertListEqual(
            [response.data, response.status_code, basket_count_before],
            [{'auth_error': 'Пользователь не аутентифицирован'}, status.HTTP_200_OK, basket_count_after]
        )

    def test_api_route_named__basket__delete_request_with_count_with_auth_permission(self):
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        data = {'id': '1',
                'count': '2'}
        url = reverse('api:basket')
        full_url = f'{url}?id={data["id"]}&count={data["count"]}'

        basket_count_before = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        response = self.client.delete(full_url, format='json')

        basket_count_after = Basket.objects.get(user=self.user) \
            .basketproducts_set.get(product__id=data['id']).count_in_basket

        self.assertListEqual(
            [response.status_code, response.data.dict(), basket_count_after],
            [status.HTTP_200_OK, data, basket_count_before - int(data['count'])]
        )
