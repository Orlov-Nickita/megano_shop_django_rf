from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Avatar(models.Model):
    """
    Модель Аватар
    """
    src = models.ImageField(upload_to='avatars/', verbose_name=_('Аватар'), default=None, null=True)
    alt = models.CharField(max_length=200, verbose_name=_('описание изображения'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))

    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('Аватарка')
        verbose_name_plural = _('Аватарки')

    def __str__(self):
        """
        Возвращается строка с никнеймом пользователя
        """
        return '{}{}'.format(_('Аватарка пользователя '), self.user.username)


class Profile(models.Model):
    """
    Модель Профиль
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    patronymic = models.CharField(max_length=20, verbose_name=_('отчество'))
    phone = models.CharField(max_length=12,
                             unique=True,
                             validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")], verbose_name=_('телефон'))

    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')

    def __str__(self):
        """
        Возвращается строка с никнеймом пользователя
        """
        return '{}{}'.format(_('Доп.инфо пользователя '), self.user.username)
