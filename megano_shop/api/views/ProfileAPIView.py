from django.contrib.auth.models import User
from django.urls import reverse
import re
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import UserSerializer, ProfileSerializer, AvatarSerializer, OrderSerializer
from frontend.models import Order
from megano_shop.settings import logger
from users.models import Profile, Avatar

from django.utils.decorators import method_decorator
from django.db.transaction import atomic


@method_decorator(atomic, name='dispatch')
class ProfileAPIView(APIView):
    """
    Представление для получения информации о профиле Пользователя, а также для изменения существующих данных
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if self.request.user.is_anonymous:
            return Response(data='Пользователь не аутентифицирован')
        user = User.objects.get(id=request.user.id)
        user_ser = UserSerializer(user).data
        profile = Profile.objects.get_or_create(user=user)[0]
        profile_ser = ProfileSerializer(profile).data
        avatar = Avatar.objects.get_or_create(user=user)[0]
        avatar_ser = AvatarSerializer(avatar).data

        orders_dict = {}

        if request.path == reverse('api:profile') and avatar_ser.get('src'):
            avatar_url = f"{request.scheme}://{request.get_host()}{avatar_ser.get('src')}"
            avatar_ser['src'] = avatar_url

        elif request.path == reverse('api:account'):
            orders_qs = Order.objects.prefetch_related('products').filter(user=request.user)
            orders_dict = {
                'orders': OrderSerializer(orders_qs, many=True).data
            }

        data = {**user_ser,
                **profile_ser,
                'avatar': {**avatar_ser},
                **orders_dict,
                }
        logger.info('Загружены данные профиля',
                    username=self.request.user.username)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        new_profile = {
            'patronymic': request.data.pop('patronymic'),
            'phone': '+{}'.format(re.sub('\D', '', request.data.pop('phone')))
        }
        new_user = {
            'username': request.user.username,
            **request.data
        }

        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=user)

        user_ser = UserSerializer(data=new_user, instance=user)
        if user_ser.is_valid(raise_exception=True):
            user_ser.save()
            profile_ser = ProfileSerializer(data=new_profile, instance=profile)
            if profile_ser.is_valid(raise_exception=True):
                profile_ser.save()
                logger.info('Обновлены данные профиля',
                            username=self.request.user.username)
                return Response(data={**user_ser.data, **profile_ser.data}, status=status.HTTP_200_OK)

            logger.error(f'Произошла ошибка {profile_ser.errors} при валидации профиля',
                         username=self.request.user.username)
            return Response(profile_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        logger.error(f'Произошла ошибка {user_ser.errors} при валидации пользователя',
                     username=self.request.user.username)
        return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)
