from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    """
    Форма для регистрации пользователя
    """
    first_name = forms.CharField(max_length=30,
                                 label=_('Имя'),
                                 required=True)

    last_name = forms.CharField(max_length=30,
                                label=_('Фамилия'),
                                required=True)

    patronymic = forms.CharField(max_length=30,
                                 label=_('Отчество'),
                                 required=False)

    email = forms.EmailField(required=True)

    phone = forms.CharField(label=_('Телефон'),
                            required=True,
                            widget=(forms.TextInput(attrs={'class': 'phone_reg_form'})))

    avatar = forms.ImageField(
        label=_('Аватар'),
        required=False)

    class Meta:
        model = User
        fields = ('username', 'avatar', 'first_name', 'last_name',
                  'patronymic', 'phone', 'email', 'password1', 'password2')
