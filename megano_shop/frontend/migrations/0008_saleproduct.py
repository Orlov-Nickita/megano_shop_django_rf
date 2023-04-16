# Generated by Django 4.1.7 on 2023-03-30 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salePrice', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='цена со скидкой')),
                ('dateFrom', models.DateTimeField(verbose_name='дата начала распродажи')),
                ('dateTo', models.DateTimeField(verbose_name='дата окончания распродажи')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_sale', to='frontend.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'товар на распродаже',
                'verbose_name_plural': 'товары на распродаже',
            },
        ),
    ]
