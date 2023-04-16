# Generated by Django 4.1.7 on 2023-03-30 19:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frontend', '0009_deliverycost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='номер заказа')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('fullname', models.CharField(default='', max_length=100, verbose_name='заказчик')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='телефон')),
                ('deliveryType', models.CharField(choices=[('', 'Not Chosen'), ('Обычная', 'Обычная'), ('Экспресс', 'Экспресс')], default='', max_length=20, verbose_name='тип доставки')),
                ('freeDelivery', models.BooleanField(default=False, verbose_name='бесплатная доставка')),
                ('paymentType', models.CharField(choices=[('', 'Not Chosen'), ('Онлайн картой', 'Онлайн картой'), ('Онлайн с чужого счета', 'Онлайн с чужого счета')], default='', max_length=40, verbose_name='способ оплаты')),
                ('totalCost', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='стоимость товаров')),
                ('deliveryCost', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='стоимость доставки')),
                ('status', models.CharField(choices=[('Заказ оплачен', 'Заказ оплачен'), ('Заказ не оплачен', 'Заказ не оплачен')], default='Заказ не оплачен', max_length=20, verbose_name='статус оплаты')),
                ('city', models.CharField(max_length=40, verbose_name='город доставки')),
                ('address', models.CharField(max_length=150, verbose_name='адрес доставки')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('count_in_order', models.PositiveIntegerField(default=0, verbose_name='количество товара в заказе')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.order', verbose_name='заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'товар из заказа',
                'verbose_name_plural': 'все товары из заказа',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='order_products', through='frontend.OrderProducts', to='frontend.product', verbose_name='товары в заказе'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]