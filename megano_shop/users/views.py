from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
import re
from django.urls import reverse_lazy
from django.views.generic import CreateView
from megano_shop.settings import logger
from users.forms import RegistrationForm
from users.models import Profile, Avatar
from django.utils.translation import gettext_lazy as _


class RegistrationView(CreateView):
    """
    Представление для регистрации новых пользователей
    """
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('frontend:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        patronymic = form.cleaned_data.get('patronymic')
        phone = re.sub('\D', '', form.cleaned_data.get('phone'))[1:]

        user = authenticate(self.request,
                            username=username,
                            password=password)

        Profile.objects.create(
            user=self.object,
            phone=phone,
            patronymic=patronymic,
        )

        if self.request.FILES.get('avatar'):
            Avatar.objects.create(
                user=self.object,
                src=self.request.FILES.get('avatar'),
                alt=f'{self.object} avatar'
            )

        login(self.request, user=user)
        logger.info(_(f'В системе зарегистрирован новый пользователь'),
                    username=username)
        return response


class MyLoginView(LoginView):
    """
    Представление для аутентификации пользователей
    """
    template_name = 'users/login_from.html'

    def form_valid(self, form):
        a = super().form_valid(form)
        logger.info(_(f'Пользователь залогинился'),
                    username=self.request.user.username)
        return a
