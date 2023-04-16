from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests, TEST_PASSWORD
from frontend.models import Product


class TestReviewAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__product_review__post_request_without_auth_permission(self):
        url = reverse(f'api:product_review', kwargs={'pk': 1})
        data = {'author': 'Nikita', 'email': 'o.rlow@ya.ru', 'text': 'asd', 'rate': 5}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_route_named__product_review__good_post_request_with_auth_permission(self):
        product_id = 1
        url = reverse(f'api:product_review', kwargs={'pk': product_id})
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        data = {'author': 'Nikita', 'email': 'o.rlow@ya.ru', 'text': 'asd', 'rate': 5}
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.get(id=product_id).reviews.get(author=data['author']))

    def test_api_route_named__product_review__bad_post_request_with_auth_permission(self):
        product_id = 1
        url = reverse(f'api:product_review', kwargs={'pk': product_id})
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        data = [
            {'author': '', 'email': 'o.rlow@ya.ru', 'text': 'asd', 'rate': 2},
            {'author': 'Nikita', 'email': 'o.rlow@ya', 'text': 'asd', 'rate': 2},
            {'author': 'Nikita', 'email': '', 'text': 'asd', 'rate': 2},
            {'author': 'Nikita', 'email': 'o.rlow@ya.ru', 'text': '', 'rate': 2},
            {'author': 'Nikita', 'email': 'o.rlow@ya.ru', 'text': 'asd', 'rate': 0},
            {'author': 'Nikita', 'email': 'o.rlow@ya.ru', 'text': 'asd', 'rate': 6},
        ]
        for i in data:
            response = self.client.post(path=url, data=i, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
