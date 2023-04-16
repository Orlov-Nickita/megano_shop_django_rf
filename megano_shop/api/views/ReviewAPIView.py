from django.db.models import Avg
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ReviewSerializer
from frontend.models import Review, Product
from megano_shop.settings import logger

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class ReviewAPIView(CreateAPIView):
    """
    Представление для публикации отзыва
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        data = request.data
        current_product_qs = Product.objects \
            .only('reviews', 'rating') \
            .prefetch_related('reviews') \
            .filter(id=pk)

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            current_product_qs.get().reviews.create(**data)
            avg_rate_cur_prod = current_product_qs.aggregate(avg_rate=Avg('reviews__rate')).get('avg_rate')
            current_product_qs.update(rating=avg_rate_cur_prod)
            logger.info(f'Пользователь добавил отзыв {data.get("text")} к товару {current_product_qs.get().title}',
                        username=self.request.user.username)
            return Response({**data}, status=status.HTTP_201_CREATED)

        logger.error(f'Произошла ошибка {serializer.errors} валидации отзыва',
                     username=self.request.user.username)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
