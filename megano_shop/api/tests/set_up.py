import datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.urls import include, path
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from frontend.models import Category, Product, DeliveryCost, Order, Basket, Tag, SaleProduct
from megano_shop.settings import TIME_ZONE
from users.models import Profile

TEST_PASSWORD = 'TestPass'


# post|delete : OrdersAPIView,

class MeganoAPIRoutesTests(APITestCase, URLPatternsTestCase):
    user = None
    urlpatterns = [
        path("", include("frontend.urls")),
        path('api/', include('api.urls')),
        path('users/', include('users.urls')),
    ]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        user = User.objects.create_user(
            username='TestCase',
            first_name='Nikita',
            last_name='Orlov',
            email='test@test.ru',
            password=TEST_PASSWORD,
        )
        cls.user = user
        Profile.objects.create(
            user=cls.user,
            phone='+79999999999',
            patronymic='Yurievich',
        )

        Tag.objects.create(name='tag_1_name', id='tag_1_id')
        Tag.objects.create(name='tag_2_name', id='tag_2_id')
        cat_1 = Category.objects.create(title='Test subcategory 1', is_subcategory=True)
        cat_2 = Category.objects.create(title='Test subcategory 2', is_subcategory=True)
        main_cat_1 = Category.objects.create(title='Test category', is_subcategory=False)
        main_cat_2 = Category.objects.create(title='Test category 2', is_subcategory=False)
        main_cat_1.subcategories.set(Category.objects.filter(id=cat_1.id))
        main_cat_2.subcategories.set(Category.objects.filter(id=cat_2.id))

        date = datetime.datetime.strptime('20:00 16-04', "%H:%M %d-%m").replace(tzinfo=pytz.timezone(TIME_ZONE))

        Product.objects.create(category=cat_1, price=100, count_in_stock=10, title='product title',
                               description='product description', fullDescription='product fullDescription',
                               freeDelivery=True, rating=0, limited=False, banner=True, available=True)
        Product.objects.create(category=cat_1, price=1000, count_in_stock=20, title='product title 2',
                               description='product description 2', fullDescription='product fullDescription 2',
                               freeDelivery=True, rating=2, limited=True, banner=True, available=True)
        Product.objects.create(category=cat_2, price=10000, count_in_stock=30, title='product title 3',
                               description='product description 3', fullDescription='product fullDescription 3',
                               freeDelivery=False, rating=4, limited=False, banner=False, available=True)

        SaleProduct.objects.create(
            product=Product.objects.get(id=1),
            salePrice=50,
            dateFrom=date,
            dateTo=date + relativedelta(days=5)
        )

        del_1 = DeliveryCost.objects.create(title=DeliveryCost.KeyWordsChoice.USUAL, money=200, description='')
        DeliveryCost.objects.create(title=DeliveryCost.KeyWordsChoice.EXPRESS, money=500, description='')
        DeliveryCost.objects.create(title=DeliveryCost.KeyWordsChoice.BASKET, money=2000, description='')

        basket = Basket.objects.create(user=user)
        basket.products.set(Product.objects.filter(id__lte=2))
        for i in Basket.objects.get(user=user).basketproducts_set.all():
            i.count_in_basket = i.id * 5
            i.save()
        a = Basket.objects\
            .filter(user=user)\
            .aggregate(basket_sum=Sum(F('basketproducts__count_in_basket') * F('basketproducts__product__price')))

        order_1 = Order.objects.create(
            user=user, orderId=1, fullname=f'{user.last_name} {user.first_name} {user.profile.patronymic}',
            email=user.email, phone=user.profile.phone, deliveryType=Order.DeliveryTypeChoice.USUAL, freeDelivery=False,
            paymentType=Order.PaymentTypeChoice.ONLINE, totalCost=a['basket_sum'], deliveryCost=del_1.money,
            status=Order.StatusChoice.ACCEPTED, city='Moscow', address='Russia')
        order_2 = Order.objects.create(
            user=user, orderId=2, fullname=f'{user.last_name} {user.first_name} {user.profile.patronymic}',
            email=user.email, phone=user.profile.phone, deliveryType=Order.DeliveryTypeChoice.USUAL, freeDelivery=False,
            paymentType=Order.PaymentTypeChoice.ONLINE, totalCost=a['basket_sum'], deliveryCost=del_1.money,
            status=Order.StatusChoice.NOT_ACCEPTED, city='Moscow', address='Russia')
        for i in basket.basketproducts_set.values('product_id', 'count_in_basket'):
            order_1.orderproducts_set.create(
                product_id=i['product_id'],
                count_in_order=i['count_in_basket']
            )
            order_2.orderproducts_set.create(
                product_id=i['product_id'],
                count_in_order=i['count_in_basket']
            )
