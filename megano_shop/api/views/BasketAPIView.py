from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import BasketSerializer
from frontend.models import Basket
from megano_shop.settings import logger
from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class BasketAPIView(APIView):
    """
    Представление для получения информации о корзине Пользователя, а также для добавления и удаления продуктов (либо
    изменения количества)
    """

    def get(self, request):
        if self.request.user.is_anonymous:
            return Response(data={'auth_error': 'Пользователь не аутентифицирован'})
        basket = Basket.objects.prefetch_related('products').filter(user=request.user)
        if basket:
            basket_ser = BasketSerializer(basket.get()).data
            logger.info(f'Корзина успешно загружена: {basket_ser}',
                        username=self.request.user.username)
            return Response(basket_ser, status=status.HTTP_200_OK)
        logger.info('Корзина пользователя пустая',
                    username=self.request.user.username)
        return Response(data='Корзина пользователя пустая', status=status.HTTP_200_OK)

    def post(self, request):
        if self.request.user.is_anonymous:
            return Response(data={'auth_error': 'Пользователь не аутентифицирован'})
        product_id = request.data.get('id')
        product_count = request.data.get('count')
        basket, created = Basket.objects.prefetch_related('products').get_or_create(user_id=request.user.id)
        product, created = basket.basketproducts_set.get_or_create(product_id=product_id)
        if product.count_in_basket == product.product.count_in_stock:
            logger.info(f'Пользователь попытался добавить в корзину {product} больше, чем в наличии',
                        username=self.request.user.username)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        product.count_in_basket += product_count
        product.save()
        logger.info(f'Пользователь добавил в корзину товар: {product}',
                    username=self.request.user.username)
        return Response(request.data, status=status.HTTP_200_OK)

    def delete(self, request):
        if self.request.user.is_anonymous:
            return Response(data={'auth_error': 'Пользователь не аутентифицирован'})
        product_id = request.query_params.get('id')
        product_count = request.query_params.get('count')
        basket = Basket.objects.prefetch_related('products').get(user_id=request.user.id)
        product = basket.basketproducts_set.get(product_id=product_id)
        if product_count:
            product.count_in_basket -= int(product_count)
            product.save()
            if product.count_in_basket == 0:
                product.delete()
                basket.save()
                logger.info(f'Пользователь удалил 1 единицу товара {product} из корзины',
                            username=self.request.user.username)

        else:
            product.delete()
            basket.save()
            logger.info(f'Пользователь удалил позицию {product} из корзины',
                        username=self.request.user.username)

        return Response(request.query_params, status=status.HTTP_200_OK)
