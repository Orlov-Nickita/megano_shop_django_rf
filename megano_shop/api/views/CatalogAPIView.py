from django.db.models import Count
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet, BooleanFilter

from api.serializers import ProductShortSerializer
from frontend.models import Product, Category
from megano_shop.settings import logger


class CatalogAPIViewPagination(PageNumberPagination):
    """
    Класс для настройки пагинации Каталога
    """
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        pk = self.request.query_params.get('category')

        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'items': data,
            'currentPage': self.page.number,
            'lastPage': self.page.paginator.num_pages,
            'categoryName': Category.objects.get(id=pk).title if pk else '',
        })


class CatalogFilter(FilterSet):
    """
    Класс для настройки фильтрации вывода информации Каталога
    """
    name = CharFilter(field_name='title', lookup_expr='contains')
    minPrice = NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = NumberFilter(field_name='price', lookup_expr='lte')
    freeDelivery = BooleanFilter(field_name='freeDelivery', method='custom_filter')
    available = BooleanFilter(field_name='available', method='custom_filter')

    def custom_filter(self, queryset, name, value):
        """
        Если флаг True, то происходит фильтрация по определенному показателю, если же False, то фильтрация не
        осуществляется
        """
        if value:
            return queryset.filter(**{name: value})
        return queryset

    class Meta:
        model = Product
        fields = ['name', 'minPrice', 'maxPrice', 'freeDelivery', 'available']


class CatalogAPIView(ListAPIView):
    """
    Представление для получения каталога
    """
    filterset_class = CatalogFilter
    pagination_class = CatalogAPIViewPagination
    serializer_class = ProductShortSerializer

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Каталог загружен',
                        username=self.request.user.username)
        else:
            logger.warning('Каталог отсутствует',
                           username=self.request.user.username)
        return a

    def get_queryset(self):
        sort = self.request.query_params.get('sort')
        if self.request.query_params.get('category'):
            pk = self.request.query_params.get('category')
        else:
            pk = self.kwargs.get('pk')
        if not pk:
            queryset = Product.objects \
                .only('id', 'category', 'price', 'title', 'images', 'reviews') \
                .select_related('category') \
                .prefetch_related('images', 'reviews') \
                .all() \
                .annotate(reviews_count=Count('reviews'))
        else:
            a = [
                i['to_category_id'] for i in Category.objects
                .get(id=pk)
                .subcategory.through.objects
                .filter(from_category=pk)
                .order_by('to_category_id')
                .values('to_category_id')
            ]
            if Category.objects.get(id=pk).is_subcategory or not a:
                queryset = Product.objects \
                    .only('id', 'category', 'price', 'title', 'images', 'reviews') \
                    .select_related('category') \
                    .prefetch_related('images', 'reviews') \
                    .filter(category=pk) \
                    .annotate(reviews_count=Count('reviews'))
            else:
                queryset = Product.objects \
                    .only('id', 'category', 'price', 'title', 'images', 'reviews') \
                    .select_related('category') \
                    .prefetch_related('images', 'reviews') \
                    .filter(category_id__gte=a[0], category_id__lte=a[-1]) \
                    .annotate(reviews_count=Count('reviews'))
        if sort:
            if self.request.query_params.get('sortType') == 'inc':
                sort = f'-{sort}'
            return queryset.order_by(sort)
        return queryset
