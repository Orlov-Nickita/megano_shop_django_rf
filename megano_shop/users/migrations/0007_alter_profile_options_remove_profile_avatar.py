# Generated by Django 4.1.7 on 2023-03-31 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_avatar_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
    ]
