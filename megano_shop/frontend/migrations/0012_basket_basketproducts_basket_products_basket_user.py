# Generated by Django 4.1.7 on 2023-03-30 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0011_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'корзина с заказом',
                'verbose_name_plural': 'корзины с заказами',
            },
        ),
        migrations.CreateModel(
            name='BasketProducts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('count_in_basket', models.PositiveIntegerField(default=0, verbose_name='количество товара в корзине')),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.basket', verbose_name='корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'товары из корзины',
                'verbose_name_plural': 'товары из всех корзин',
            },
        ),
        migrations.AddField(
            model_name='basket',
            name='products',
            field=models.ManyToManyField(related_name='basket_products', through='frontend.BasketProducts', to='frontend.product', verbose_name='товары в корзине'),
        ),
        migrations.AddField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='покупатель'),
        ),
    ]