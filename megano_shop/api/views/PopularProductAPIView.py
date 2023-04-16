from django.db.models import Count
from rest_framework.generics import ListAPIView

from api.serializers import ProductShortSerializer
from frontend.models import Product
from megano_shop.settings import logger


class PopularProductAPIView(ListAPIView):
    """
    Представление для получения популярных товаров
    """
    queryset = Product.objects \
                   .only('id', 'category', 'price', 'title', 'images', 'reviews') \
                   .select_related('category') \
                   .prefetch_related('images', 'tags', 'reviews', 'specifications') \
                   .annotate(saled=Count('orderproducts__product')) \
                   .order_by('-rating', '-saled') \
                   .exclude(saled=0)[:5]
    serializer_class = ProductShortSerializer

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Популярные продукты загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Популярные продукты отсутствуют',
                           username=self.request.user.username)
        return a
