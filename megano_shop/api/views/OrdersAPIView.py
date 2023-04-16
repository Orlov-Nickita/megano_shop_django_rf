from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import OrderSerializer, OrderProductsSerializer
from frontend.models import Order, Basket, OrderProducts
from megano_shop.settings import logger

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class OrdersAPIView(APIView):
    """
    Представление для получения информации о заказе, а также для создания нового (в момент оформления заказа из
    корзины) и подтверждения (после перехода к оплате)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        if self.request.user.is_anonymous:
            return Response(data='Пользователь не аутентифицирован')
        if pk:
            order_qs = Order.objects.prefetch_related('products').get(user_id=request.user.id, orderId=pk)
            data = OrderSerializer(order_qs).data
        else:
            orders_qs = Order.objects.prefetch_related('products').filter(user_id=request.user.id)
            data = OrderSerializer(orders_qs, many=True).data
        if data:
            logger.info('История заказов загружена',
                        username=self.request.user.username)
        else:
            logger.warning('История заказов отсутствует',
                           username=self.request.user.username)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        user = User.objects.get(username=request.user.username)
        if not pk:
            basket_id = request.data.get('basketId')
            """
            В данном случае происходит подтверждение выбранных товаров из корзины и переход к формированию 
            (заполнению подробностей) заказа
            """
            basket = Basket.objects \
                .prefetch_related('products') \
                .filter(user=user, id=basket_id) \
                .annotate(basket_sum=Sum(F('basketproducts__count_in_basket') * F('basketproducts__product__price'))) \
                .get()
            data = {
                'user': user.id,
                'totalCost': basket.basket_sum,
                'fullname': f'{user.last_name} {user.first_name} {user.profile.patronymic}',
                'email': user.email,
                'phone': user.profile.phone,
                'deliveryCost': 0,
            }
            serializer_order = OrderSerializer(data=data)
            if serializer_order.is_valid(raise_exception=True):
                a = serializer_order.save()
                data_for_order_products = [
                    {'order': a.orderId,
                     'product': i,
                     'count_in_order': basket.basketproducts_set.get(product_id=i['id']).count_in_basket}
                    for i in basket.products.all().values()
                ]
                for index in range(len(data_for_order_products)):
                    serializer_order_products = OrderProductsSerializer(data=data_for_order_products[index])
                    if serializer_order_products.is_valid(raise_exception=True):
                        serializer_order_products.save()
                    else:
                        return Response(serializer_order_products.errors, status=status.HTTP_400_BAD_REQUEST)
                basket.delete()
                logger.info(f'Заказ {a.orderId} подтвержден пользователем и отправлен в оплату',
                            username=self.request.user.username)
                data = {'id': a.orderId, 'products': [i['product'] for i in data_for_order_products]}
                return Response(data=data, status=status.HTTP_200_OK)

            return Response(serializer_order.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            """
            В данном случае происходит подтверждение заказа, обновление полей модели (подробностей конкретного заказа) и 
            переход к оплате заказа
            """
            order = Order.objects \
                .prefetch_related('products') \
                .get(user=request.user, orderId=pk)
            order_products = OrderProducts.objects \
                .prefetch_related('order', 'product') \
                .filter(order=order)
            data_for_order = {
                'user': request.user.id,
                **request.data
            }
            order_id = request.data.get('orderId')
            products = request.data.get('products')
            data_for_order_products = [
                {'order': order_id,
                 'product': products[i],
                 'count_in_order': products[i].pop('count_in_order')}
                for i in range(len(products))
            ]
            serializer_order = OrderSerializer(data=data_for_order, instance=order)
            if serializer_order.is_valid(raise_exception=True):
                serializer_order.save()
                for index in range(len(data_for_order_products)):
                    serializer_order_products = OrderProductsSerializer(data=data_for_order_products[index],
                                                                        instance=order_products[index])
                    if serializer_order_products.is_valid(raise_exception=True):
                        serializer_order_products.save()

                    else:
                        logger.error(
                            f'Произошла ошибка {serializer_order_products.errors} при валидации продуктов в заказе',
                            username=self.request.user.username)
                        return Response(serializer_order_products.errors, status=status.HTTP_400_BAD_REQUEST)
                logger.info(f'Заказ {order.orderId} подтвержден пользователем и отправлен в оплату',
                            username=self.request.user.username)
                return Response(status=status.HTTP_201_CREATED)
            logger.error(f'Произошла ошибка {serializer_order.errors} при валидации заказа',
                         username=self.request.user.username)
            return Response(serializer_order.errors, status=status.HTTP_400_BAD_REQUEST)
