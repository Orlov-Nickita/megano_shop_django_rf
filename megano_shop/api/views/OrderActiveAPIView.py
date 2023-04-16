from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import OrderSerializer
from frontend.models import Order
from megano_shop.settings import logger


class OrderActiveAPIView(APIView):
    """
    Представление для получения активного заказа (последний из неоплаченных)
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        id = request.COOKIES.get('order_id_from_history')
        if not id:
            if self.request.user.is_anonymous:
                return Response(data='Пользователь не аутентифицирован')
            active_order = Order.objects \
                .prefetch_related('products') \
                .order_by('-orderId') \
                .filter(user_id=self.request.user.id,
                        status=Order.StatusChoice.NOT_ACCEPTED).first()

            if not active_order:
                logger.info('У пользователя нет активного заказа',
                            username=self.request.user.username)
                return Response('Активного заказа нет', status=status.HTTP_200_OK)

            logger.info('У пользователя имеется активный заказ',
                        username=self.request.user.username)
            order = OrderSerializer(active_order).data
            return Response(order, status=status.HTTP_200_OK)

        history_order = Order.objects \
            .prefetch_related('products') \
            .get(user_id=self.request.user.id,
                 orderId=id)
        order = OrderSerializer(history_order).data
        return Response(order, status=status.HTTP_200_OK)
