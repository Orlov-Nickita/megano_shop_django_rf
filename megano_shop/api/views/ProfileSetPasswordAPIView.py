from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ChangePasswordSerializer
from megano_shop.settings import logger

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class ProfileSetPasswordAPIView(GenericAPIView):
    """
    Представление для обновления существующего пароля
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        username = self.request.user.username
        if serializer.is_valid(raise_exception=True):
            if not request.user.check_password(serializer.data.get('passwordCurrent')):
                return Response(data='Неправильный текущий пароль!', status=status.HTTP_400_BAD_REQUEST)

            request.user.set_password(serializer.data.get('passwordNew'))
            request.user.save()
            user = authenticate(self.request,
                                username=username,
                                password=serializer.data.get('passwordNew'))
            login(self.request, user=user)
            logger.info('Пользователь поменял пароль',
                        username=self.request.user.username)
            return Response(data={'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

        logger.info(f'Произошла ошибка {serializer.errors} при валидации пароля',
                    username=self.request.user.username)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
