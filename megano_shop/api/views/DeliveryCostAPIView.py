from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from frontend.models import DeliveryCost
from megano_shop.settings import logger


class DeliveryCostAPIView(APIView):
    """
    Представление для получения стоимости доставки в зависимости от общей стоимости заказа и типа доставки
    """
    def get(self, request, total_cost, delivery_type):
        all_delivery_costs = {i.title: i.money for i in DeliveryCost.objects.all()}

        if all_delivery_costs:
            logger.info('Данные о стоимостях доставок загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Данные о стоимостях доставок отсутствуют',
                           username=self.request.user.username)

        if delivery_type == DeliveryCost.KeyWordsChoice.EXPRESS:
            delivery_cost = all_delivery_costs.get(delivery_type)

        elif delivery_type == DeliveryCost.KeyWordsChoice.USUAL \
                and total_cost < all_delivery_costs.get(DeliveryCost.KeyWordsChoice.BASKET):
            delivery_cost = all_delivery_costs.get(delivery_type)

        else:
            delivery_cost = 0

        return Response(delivery_cost, status=status.HTTP_200_OK)
