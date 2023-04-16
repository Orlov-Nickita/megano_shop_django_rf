from rest_framework.generics import ListAPIView
from api.serializers import ProductShortSerializer
from frontend.models import Product
from megano_shop.settings import logger


class BannersAPIView(ListAPIView):
    """
    Представление для отображения баннеров на главной странице
    """
    queryset = Product.objects \
        .only('id', 'category', 'price', 'title', 'images', 'reviews') \
        .select_related('category') \
        .prefetch_related('images', 'tags', 'reviews', 'specifications') \
        .filter(banner=True)
    serializer_class = ProductShortSerializer

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Банеры загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Информация о банерах отсутствует',
                           username=self.request.user.username)
        return a
