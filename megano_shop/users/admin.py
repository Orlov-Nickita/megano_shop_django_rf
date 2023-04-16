from django.contrib import admin

from users.models import Avatar, Profile


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Avatar (Аватар)
    """
    list_display = ['id', 'src', 'alt']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Profile (Профиль)
    """
    list_display = ['user', 'patronymic', 'phone']
