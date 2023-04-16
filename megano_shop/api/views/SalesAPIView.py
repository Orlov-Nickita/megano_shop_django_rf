from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from api.serializers import SaleProductSerializer
from frontend.models import SaleProduct
from megano_shop.settings import logger


class SalesAPIViewPagination(PageNumberPagination):
    """
    Класс для настройки пагинации Товаров на распродаже
    """
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages
        })


class SalesAPIView(ListAPIView):
    """
    Представление для получения Товаров на распродаже
    """
    queryset = SaleProduct.objects.prefetch_related('product').all()
    serializer_class = SaleProductSerializer
    pagination_class = SalesAPIViewPagination

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Товары с распродажи загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Информация о товарах с распродажи отсутствует',
                           username=self.request.user.username)
        return a
