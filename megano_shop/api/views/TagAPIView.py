from rest_framework.generics import ListAPIView
from api.serializers import TagSerializer
from frontend.models import Tag
from megano_shop.settings import logger


class TagAPIView(ListAPIView):
    """
    Представление для получения тегов
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        a = super().get(request, *args, **kwargs)
        if a.data:
            logger.info('Теги загружены',
                        username=self.request.user.username)
        else:
            logger.warning('Информация о тегах отсутствует',
                           username=self.request.user.username)
        return a
