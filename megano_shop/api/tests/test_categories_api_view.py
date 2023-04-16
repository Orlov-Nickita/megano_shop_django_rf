from rest_framework import status
from rest_framework.reverse import reverse

from api.tests.set_up import MeganoAPIRoutesTests
from frontend.models import Category


class TestCategoriesAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__categories__get_request(self):
        a = [
            {'id': 3, 'title': 'Test category', 'image': None, 'href': '/catalog/3', 'subcategories': [
                {'id': 1, 'title': 'Test subcategory 1', 'image': {'src': '', 'alt': ''}, 'href': '/catalog/1'}]},
            {'id': 4, 'title': 'Test category 2', 'image': None, 'href': '/catalog/4', 'subcategories': [
                {'id': 2, 'title': 'Test subcategory 2', 'image': {'src': '', 'alt': ''}, 'href': '/catalog/2'}]}
        ]
        url = reverse(f'api:categories')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == len(Category.objects.filter(is_subcategory=False)))
        self.assertEqual(response.data, a)
