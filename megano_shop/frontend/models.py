from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Модель Категория
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('категория')
        verbose_name_plural = _('категории')

    title = models.CharField(max_length=100, default='', verbose_name=_('название категории'))
    image = models.OneToOneField('CategoryImage', on_delete=models.CASCADE,
                                 default=None,
                                 null=True, blank=True,
                                 verbose_name=_('изображение категории'))
    subcategories = models.ManyToManyField('Category',
                                           default='',
                                           related_name='subcategory',
                                           blank=True,
                                           verbose_name=_('подкатегории'))
    is_subcategory = models.BooleanField(default=True, verbose_name=_('является подкатегорией'),
                                         help_text=_('Для выбора подкатегорий необходимо снять галочку и сохранить '
                                                     'выбор. После обновления страницы откроется доступ к подкатегориям'))

    def __str__(self):
        """
        Возвращает имя категории
        """
        return self.title

    def href(self):
        """
        Возвращает ссылку на объект модели Категория
        """
        return f'/catalog/{self.id}'

    href.short_description = 'URL'


class CategoryImage(models.Model):
    """
    Модель Изображение категории
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('фотография категории')
        verbose_name_plural = _('фотографии категорий')

    src = models.ImageField(upload_to='categories_picture/',
                            default=None,
                            null=True, blank=True,
                            verbose_name=_('изображение категории'))
    alt = models.CharField(max_length=200, verbose_name=_('описание изображения'))

    def __str__(self):
        """
        Возвращает описание изображения
        """
        return self.alt


class Tag(models.Model):
    """
    Модель Тег
    """
    class Meta:
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

    id = models.CharField(primary_key=True, max_length=50, verbose_name=_('id тега'))
    name = models.CharField(max_length=50, default='', verbose_name=_('имя тега'))

    def __str__(self):
        """
        Возвращает имя тега
        """
        return f'{self.name}'


class Review(models.Model):
    """
    Модель Отзыв
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('отзыв')
        verbose_name_plural = _('отзывы')

    author = models.CharField(max_length=50, verbose_name=_('автор отзыва'), default='')
    email = models.EmailField(verbose_name=_('email автора'), default='')
    text = models.TextField(max_length=500, verbose_name=_('текст отзыва'), default='')
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1),
                                                   MaxValueValidator(5)],
                                       blank=False,
                                       verbose_name=_('оценка товара'), default=0)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата отзыва'))

    def __str__(self):
        """
        Возвращает строку с указанием пользователя, которым был написан отзыв
        """
        return '{}{}'.format(_('Отзыв от '), self.author)


class ProductImage(models.Model):
    """
    Модель Изображение продукта
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('фотография товара')
        verbose_name_plural = _('фотографии товаров')

    file = models.ImageField(upload_to='product_picture/', verbose_name=_('изображение товара'))
    alt = models.CharField(max_length=200, verbose_name=_('описание изображения'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строку c названием фото
        """
        return '{}{}'.format(_('Фото '), self.file)


class Specifications(models.Model):
    """
    Модель Характеристики
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('характеристика')
        verbose_name_plural = _('характеристики')

    name = models.CharField(max_length=100, verbose_name=_('название характеристики'))
    value = models.CharField(max_length=100, verbose_name=_('значение'))

    def __str__(self):
        """
        Возвращает строку типа "название характеристики - значение"
        """
        return f'{self.name} - {self.value}'


class Product(models.Model):
    """
    Модель Продукт
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('товар')
        verbose_name_plural = _('товары')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('категория товара'), default='',
                                 null=True, related_name='category')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('цена'))
    count_in_stock = models.IntegerField(verbose_name=_('количество в наличии'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    title = models.CharField(max_length=150, verbose_name=_('название'))
    description = models.CharField(max_length=150, verbose_name=_('краткое описание'))
    fullDescription = models.TextField(verbose_name=_('полное описание'))
    freeDelivery = models.BooleanField(default=False, verbose_name=_('бесплатная доставка'))
    images = models.ManyToManyField(ProductImage, verbose_name=_('изображения товара'), blank=True,
                                    related_name='product_image')
    tags = models.ManyToManyField(Tag, verbose_name=_('тег'), blank=True, related_name='product_tags')
    reviews = models.ManyToManyField(Review, verbose_name=_('отзывы'), blank=True, related_name='product_reviews')
    rating = models.DecimalField(decimal_places=1, max_digits=2, verbose_name=_('рейтинг'), blank=True, null=True,
                                 default=0,
                                 validators=[MinValueValidator(0),
                                             MaxValueValidator(5)])
    limited = models.BooleanField(default=False, verbose_name=_('ограниченный тираж'))
    banner = models.BooleanField(default=False, verbose_name=_('баннер на главной странице'))
    specifications = models.ManyToManyField(Specifications, verbose_name=_('дополнительные характеристики'), blank=True,
                                            related_name='product_specs')
    available = models.BooleanField(default=True, verbose_name=_('в наличии'))

    def href(self):
        """
        Возвращает ссылку на объект модели Продукт
        """
        return f'/product/{self.id}'

    def __str__(self):
        """
        Возвращает название продукта
        """
        return self.title


class SaleProduct(models.Model):
    """
    Модель Товар на распродаже (Распродажа)
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('товар на распродаже')
        verbose_name_plural = _('товары на распродаже')

    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='product_sale',
                                   verbose_name=_('товар'))
    salePrice = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('цена со скидкой'))
    dateFrom = models.DateTimeField(verbose_name=_('дата начала распродажи'))
    dateTo = models.DateTimeField(verbose_name=_('дата окончания распродажи'))

    def __str__(self):
        """
        Возвращает строку содержащую название товара, который участвует в распродаже
        """
        return '{}{}'.format(_('Уценка на '), self.product.title)


class DeliveryCost(models.Model):
    """
    Модель Стоимость доставки
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('стоимость доставки')
        verbose_name_plural = _('стоимости доставки')

    class KeyWordsChoice(models.TextChoices):
        """
        Класс создающий перечень строк (1,2 для определения стоимости доставки и 3 для определения общей стоимости
        товаров в корзине, при которой действует бесплатная доставка)
        """
        USUAL = 'Обычная', _('Обычная')
        EXPRESS = 'Экспресс', _('Экспресс')
        BASKET = 'Корзина', _('Корзина')

    title = models.CharField(max_length=100, choices=KeyWordsChoice.choices,
                             verbose_name=_('название величины'))
    money = models.DecimalField(decimal_places=2, max_digits=10, verbose_name=_('сумма'))
    description = models.TextField(max_length=100, verbose_name=_('описание'))

    def __str__(self):
        """
        Возвращает название величины из модели Стоимость доставки
        """
        return self.title


class Order(models.Model):
    """
    Модель Заказ
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    class DeliveryTypeChoice(models.TextChoices):
        """
        Класс создающий перечень строк для определения типа доставки
        """
        NOT_CHOSEN = ''
        USUAL = 'Обычная', _('Обычная')
        EXPRESS = 'Экспресс', _('Экспресс')

    class PaymentTypeChoice(models.TextChoices):
        """
        Класс создающий перечень строк для определения типа оплаты
        """
        NOT_CHOSEN = ''
        ONLINE = 'Онлайн картой', _('Онлайн картой')
        ONLINE_SOMEONE_ELSE_ACC = 'Онлайн с чужого счета', _('Онлайн с чужого счета')

    class StatusChoice(models.TextChoices):
        """
        Класс создающий перечень строк для определения завершенности оплаты
        """
        ACCEPTED = 'Заказ оплачен', _('Заказ оплачен')
        NOT_ACCEPTED = 'Заказ не оплачен', _('Заказ не оплачен')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    orderId = models.AutoField(primary_key=True, unique=True, verbose_name=_('номер заказа'))
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    fullname = models.CharField(max_length=100, default='', verbose_name=_('заказчик'))
    email = models.EmailField(verbose_name='email')
    phone = models.CharField(max_length=16,
                             validators=[RegexValidator(regex=r"^\+?1?\d{8,15}$")], verbose_name=_('телефон'))
    deliveryType = models.CharField(max_length=20, choices=DeliveryTypeChoice.choices,
                                    default=DeliveryTypeChoice.NOT_CHOSEN, verbose_name=_('тип доставки'))
    freeDelivery = models.BooleanField(default=False, verbose_name=_('бесплатная доставка'))
    paymentType = models.CharField(max_length=40, choices=PaymentTypeChoice.choices,
                                   default=PaymentTypeChoice.NOT_CHOSEN, verbose_name=_('способ оплаты'))
    totalCost = models.DecimalField(decimal_places=2, max_digits=20, verbose_name=_('стоимость товаров'))
    deliveryCost = models.DecimalField(decimal_places=2, max_digits=6,
                                       verbose_name=_('стоимость доставки'), default=0)
    status = models.CharField(max_length=20, choices=StatusChoice.choices,
                              default=StatusChoice.NOT_ACCEPTED, verbose_name=_('статус оплаты'))
    city = models.CharField(max_length=40, verbose_name=_('город доставки'), blank=True)
    address = models.CharField(max_length=150, verbose_name=_('адрес доставки'), blank=True)
    products = models.ManyToManyField(Product, verbose_name=_('товары в заказе'),
                                      through='OrderProducts', related_name='order_products')

    def __str__(self):
        """
        Возвращается строка с номером заказа
        """
        return '{}{}'.format(_('Заказ # '), self.orderId)


class Payment(models.Model):
    """
    Модель Платеж
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('платеж')
        verbose_name_plural = _('платежи')

    number = models.CharField(max_length=20, verbose_name=_('номер карты'))
    name = models.CharField(max_length=150, verbose_name=_('имя держателя карты'))
    month = models.CharField(max_length=2, verbose_name=_('месяц'))
    year = models.CharField(max_length=4, verbose_name=_('год'))
    code = models.CharField(max_length=10, verbose_name=_('cvv код'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment', verbose_name=_('заказ'))
    status = models.BooleanField(default=False, verbose_name=_('статус оплаты'))
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name=_('дата создания'))
    paid_for = models.DecimalField(decimal_places=2, max_digits=12, default=0, verbose_name=_('сумма платежа'))

    def __str__(self):
        """
        Возвращается строка с платежной информацией конкретного пользователя и по определенному заказу
        """
        return '{} {} {} {}'.format(_('Платежная информация пользователя'),
                                    self.user.username,
                                    _('по заказу'),
                                    self.order.orderId)


class Basket(models.Model):
    """
    Модель Корзина
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('корзина с заказом')
        verbose_name_plural = _('корзины с заказами')

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('покупатель'))
    products = models.ManyToManyField(Product, verbose_name=_('товары в корзине'),
                                      through='BasketProducts', related_name=_('basket_products'))

    def __str__(self):
        """
        Возвращается строка с номером корзины
        """
        return '{}{}'.format(_('Корзина #'), self.id)


class BasketProducts(models.Model):
    """
    Модель Продукты в корзине
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('товар из корзины')
        verbose_name_plural = _('все товары из корзины')

    id = models.AutoField(primary_key=True, unique=True)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name=_('корзина'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    count_in_basket = models.PositiveIntegerField(default=0, verbose_name=_('количество товара в корзине'))

    def __str__(self):
        """
        Возвращается название товара
        """
        return f'{self.product}'


class OrderProducts(models.Model):
    """
    Модель Продукты в заказе
    """
    class Meta:
        """
        Метакласс для определения названий в единственном и множественном числе
        """
        verbose_name = _('товар из заказа')
        verbose_name_plural = _('все товары из заказа')

    id = models.AutoField(primary_key=True, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('заказ'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    count_in_order = models.PositiveIntegerField(default=0, verbose_name=_('количество товара в заказе'))

    def __str__(self):
        """
        Возвращается название товара
        """
        return f'{self.product}'
