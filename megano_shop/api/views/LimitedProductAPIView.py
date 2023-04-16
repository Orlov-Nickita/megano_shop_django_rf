from rest_framework.generics import ListAPIView

from api.serializers import ProductShortSerializer
from frontend.models import Product
from megano_shop.settings import logger


class LimitedProductAPIView(ListAPIView):
    """
    Представление для получения лимитированных товаров
    """
    queryset = Product.objects \
                   .only('id', 'category', 'price', 'title', 'images', 'reviews') \
                   .select_related('category') \
                   .prefetch_related('images', 'tags', 'reviews', 'specifications') \
                   .filter(limited=True) \
                   .order_by('-id')[:16]
    serializer_class = ProductShortSerializer

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Продукты с ограниченным тиражом загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Продукты с ограниченным тиражом отсутствуют',
                           username=self.request.user.username)
        return a
