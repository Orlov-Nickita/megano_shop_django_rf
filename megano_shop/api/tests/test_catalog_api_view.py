from rest_framework import status
from rest_framework.reverse import reverse
from api.tests.set_up import MeganoAPIRoutesTests
from frontend.models import Product


class TestCatalogAPIView(MeganoAPIRoutesTests):
    def test_api_route_named__catalog__get_request(self):
        a = [{'id': 1, 'price': 100, 'title': 'product title', 'href': '/product/1', 'images': []},
             {'id': 2, 'price': 1000, 'title': 'product title 2', 'href': '/product/2', 'images': []},
             {'id': 3, 'price': 10000, 'title': 'product title 3', 'href': '/product/3', 'images': []}]

        url = reverse(f'api:catalog')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) == len(Product.objects.all()))
        self.assertEqual(response.data, a)

    def test_api_route_named__catalog__get_request_with_parameters(self):

        query = [
            {'page': 1, 'category': 1, 'sort': 'price', 'sortType': 'inc', 'name': '', 'minPrice': 1,
             'maxPrice': 200000, 'freeDelivery': 'false', 'available': 'true', 'limit': 8},
            {'page': 1, 'category': 1, 'sort': 'price', 'sortType': 'dec', 'name': '', 'minPrice': 1,
             'maxPrice': 200000, 'freeDelivery': 'false', 'available': 'true', 'limit': 8},
            {'page': 1, 'category': '', 'sort': 'rating', 'sortType': 'inc', 'name': '', 'minPrice': 1,
             'maxPrice': 200000, 'freeDelivery': 'false', 'available': 'true', 'limit': 8},
            {'page': 1, 'category': '', 'sort': 'price', 'sortType': 'dec', 'name': '', 'minPrice': 900,
             'maxPrice': 1100, 'freeDelivery': 'false', 'available': 'true', 'limit': 8},
            {'page': 1, 'category': '', 'sort': 'price', 'sortType': 'inc', 'name': '', 'minPrice': 1,
             'maxPrice': 200000, 'freeDelivery': 'false', 'available': 'true', 'limit': 2},
        ]
        data = [
            {'links': {'next': None, 'previous': None},
             'count': 2,
             'items': [{'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': []},
                       {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': []}],
             'currentPage': 1,
             'lastPage': 1,
             'categoryName': 'Test subcategory 1'
             },
            {'links': {'next': None, 'previous': None},
             'count': 2,
             'items': [{'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': []},
                       {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': []}],
             'currentPage': 1,
             'lastPage': 1,
             'categoryName': 'Test subcategory 1'
             },
            {'links': {'next': None, 'previous': None},
             'count': 3,
             'items': [{'id': 3, 'price': 10000.0, 'title': 'product title 3', 'href': '/product/3', 'images': []},
                       {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': []},
                       {'id': 1, 'price': 100.0, 'title': 'product title', 'href': '/product/1', 'images': []}],
             'currentPage': 1,
             'lastPage': 1,
             'categoryName': ''
             },
            {'links': {'next': None, 'previous': None},
             'count': 1,
             'items': [{'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': []}],
             'currentPage': 1,
             'lastPage': 1,
             'categoryName': ''
             },
            {'links': {'next': None, 'previous': None},
             'count': 3,
             'items': [{'id': 3, 'price': 10000.0, 'title': 'product title 3', 'href': '/product/3', 'images': []},
                       {'id': 2, 'price': 1000.0, 'title': 'product title 2', 'href': '/product/2', 'images': []}],
             'currentPage': 1,
             'lastPage': 2,
             'categoryName': ''
             }
        ]

        url = reverse(f'api:catalog')
        for i in range(len(query)):
            if i == len(query) - 1:
                sorted_keys = list(query[i].keys())
                sorted_keys.sort()
                sorted_dict = {j: query[i][j] for j in sorted_keys}
                if len(Product.objects.all()) % sorted_dict['limit'] != 0:
                    sorted_dict['page'] += 1
                query_list = '&'.join([f"{key}={value}" for (key, value) in sorted_dict.items()])
                data[i]['links']['next'] = f"http://testserver{reverse('api:catalog')}?{query_list}"

            response = self.client.get(path=url, data=query[i], format='json')
            self.assertEqual(response.data, data[i])

    def test_api_route_named__catalog_num__get_request(self):
        a = [{'id': 1, 'price': 100, 'title': 'product title', 'href': '/product/1', 'images': []},
             {'id': 2, 'price': 1000, 'title': 'product title 2', 'href': '/product/2', 'images': []}]
        url = reverse('api:catalog_num', kwargs={'pk': 1})
        response = self.client.get(url, format='json')

        b = [{'id': 3, 'price': 10000, 'title': 'product title 3', 'href': '/product/3', 'images': []}]
        url_2 = reverse('api:catalog_num', kwargs={'pk': 2})
        response_2 = self.client.get(url_2, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, a)
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, b)
