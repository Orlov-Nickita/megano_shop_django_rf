from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import ProductSerializer
from frontend.models import Product


class ProductAPIView(APIView):
    """
    Представление для получения информации о конкретном товаре
    """
    def get(self, request, pk):
        queryset = Product.objects \
            .select_related('category') \
            .prefetch_related('images', 'tags', 'reviews', 'specifications') \
            .get(id=pk)
        qs_ser = ProductSerializer(queryset).data
        return Response(qs_ser, status=status.HTTP_200_OK)
