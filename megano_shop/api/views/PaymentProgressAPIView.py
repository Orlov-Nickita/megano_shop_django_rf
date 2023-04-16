import random

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend.models import Payment, Order
from megano_shop.settings import logger

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class PaymentProgressAPIView(APIView):
    """
    Представление для подтверждения осуществляемого платежа (проверяются введенные данные)
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pay_id = request.data.get('payment_id')
        pay = Payment.objects \
            .prefetch_related('order') \
            .get(id=pay_id, user_id=request.user.id)

        if int(pay.number) % 2 == 0 and pay.number[-1] != '0':
            pay.order.status = Order.StatusChoice.ACCEPTED
            pay.status = True
            pay.order.save()
            pay.save()

            logger.info(f'Платеж {pay_id} принят, заказ оплачен',
                        username=self.request.user.username)
            return Response(data='Заказ успешно подтвержден и оплачен',
                            status=status.HTTP_202_ACCEPTED)

        logger.info(f'Платеж {pay_id} не принят, данные банковского счета некорректны - заказ не оплачен',
                    username=self.request.user.username)
        errors = [
            'На карте недостаточно средств. Пожалуйста, попробуйте оплатить заказ другой картой',
            'При обработке платежа произошла ошибка',
            'Неправильно заполнены реквизиты банковской карты',
            'Счета с таким идентификатором не существует',
            'Оплата с использованием корпоративных карт запрещена. Необходимо использовать другую карту',
            'Превышено допустимое время оплаты по данному коду платежа',
        ]
        return Response(data=random.choice(errors), status=status.HTTP_503_SERVICE_UNAVAILABLE)
