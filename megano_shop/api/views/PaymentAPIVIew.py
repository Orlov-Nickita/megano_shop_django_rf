from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PaymentSerializer
from megano_shop.settings import logger

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class PaymentAPIVIew(APIView):
    """
    Представление для создания нового платежа
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if (int(request.data.get('year')) > 2023 or int(request.data.get('year')) < 2018) \
                or (int(request.data.get('month')) > 12 or int(request.data.get('month')) <= 0):
            return Response(data='Неверно указан год или месяц', status=status.HTTP_400_BAD_REQUEST)
        serializer_payment = PaymentSerializer(data={**request.data, 'user': request.user.id})
        if serializer_payment.is_valid(raise_exception=True):
            serializer_payment.save()
            payment_id = serializer_payment.data.get('id')
            order_id = serializer_payment.data.get('order')

            response = Response(data={'payment_id': payment_id}, status=status.HTTP_201_CREATED)
            response.set_cookie('payment_id', payment_id, 180)
            response.set_cookie('order_id', order_id, 180)
            logger.info(f'Данные банковского счета по платежу {payment_id} по заказу {order_id} приняты в обработку',
                        username=self.request.user.username)
            return response

        logger.error(f'Произошла ошибка {serializer_payment.errors} при валидации платежа',
                     username=self.request.user.username)
        return Response(status=status.HTTP_400_BAD_REQUEST)
