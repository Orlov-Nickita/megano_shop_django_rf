from rest_framework.generics import ListAPIView

from api.serializers import CategorySerializer
from frontend.models import Category
from megano_shop.settings import logger


class CategoriesAPIView(ListAPIView):
    """
    Представление для получения категориях и подкатегориях
    """
    queryset = Category.objects \
        .select_related('image') \
        .prefetch_related('subcategories') \
        .filter(is_subcategory=False)
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Категории загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Категории отсутствуют',
                           username=self.request.user.username)
        return a
