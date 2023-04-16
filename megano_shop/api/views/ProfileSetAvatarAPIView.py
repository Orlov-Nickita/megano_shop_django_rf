from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import AvatarSerializer
from megano_shop.settings import logger
from users.models import Avatar

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class ProfileSetAvatarAPIView(GenericAPIView):
    """
    Представление для добавления или удаления аватара Пользователя
    """
    parser_classes = [MultiPartParser, FileUploadParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        file_avatar = request.FILES.get('file')

        user = User.objects.get(username=request.user)
        user_avatar = Avatar.objects.get_or_create(user=user)[0]

        data = {
            'src': file_avatar,
            'alt': f'{user.username} avatar'
        }
        serializer = AvatarSerializer(data=data, instance=user_avatar)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info('Добавлен аватар пользователя',
                        username=self.request.user.username)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        logger.error(f'Произошла ошибка {serializer.errors} при валидации аватарки',
                     username=self.request.user.username)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user_avatar = Avatar.objects.get(user=request.user)
        user_avatar.delete()
        logger.info('Удален аватар пользователя',
                    username=self.request.user.username)
        return Response(status=status.HTTP_200_OK)
