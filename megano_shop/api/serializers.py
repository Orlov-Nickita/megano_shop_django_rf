from urllib.parse import unquote
from django.contrib.auth.models import User
from rest_framework import serializers
from frontend.models import Category, Tag, Product, Review, CategoryImage, ProductImage, Order, Basket, BasketProducts, \
    OrderProducts, Payment, Specifications, SaleProduct
from users.models import Profile, Avatar


class CategoryImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели CategoryImage
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = CategoryImage
        fields = ['src', 'alt']

    def to_representation(self, instance):
        """
        Переопределяет представление модели CategoryImage
        """
        a = super().to_representation(instance)
        a['src'] = unquote(a['src'])
        return a


class SubcategoriesField(serializers.RelatedField):
    """
    Кастомное представление реляционного поля Subcategories модели Category
    """
    def to_representation(self, value):
        """
        Переопределяет представление реляционного поля Subcategories модели Category
        """
        if not value.image:
            temp = {
                'src': '',
                'alt': ''
            }
        else:
            temp = CategoryImageSerializer(value.image).data
            req = self.context.get('request')
            base_url = f"{req.scheme}://{req.get_host()}"
            temp['src'] = unquote(base_url + temp['src'])

        return {
            'id': value.id,
            'title': value.title,
            'image': temp,
            'href': value.href(),
        }


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category
    """
    image = CategoryImageSerializer(read_only=True)
    subcategories = SubcategoriesField(many=True, read_only=True)

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Category
        fields = ['id', 'title', 'image', 'href', 'subcategories']


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Tag
        fields = ['id', 'name']


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ProductImage
    """
    file = serializers.ImageField(use_url=True)

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = ProductImage
        fields = ['file']

    def to_representation(self, instance):
        """
        Переопределяет представление модели ProductImage
        """
        a = super().to_representation(instance)
        return a['file']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Review
    """
    date = serializers.DateTimeField(read_only=True, format="%H:%M %d-%m-%Y")

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'date']


class SpecificationsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Specifications
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Specifications
        fields = ['name', 'value']


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product
    """
    id = serializers.IntegerField()
    date = serializers.DateTimeField(read_only=True, format="%H:%M %d-%m-%Y")
    reviews = ReviewSerializer(many=True)
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = SpecificationsSerializer(many=True, read_only=True)
    price = serializers.FloatField()
    rating = serializers.FloatField()

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Product
        fields = ['id', 'category', 'price', 'count_in_stock', 'date', 'title', 'description',
                  'fullDescription', 'available', 'freeDelivery', 'rating', 'href',
                  'specifications', 'reviews', 'images', 'tags']


class ProductShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product - сокращенная версия
    """
    id = serializers.IntegerField()
    images = ProductImageSerializer(many=True, read_only=True)
    price = serializers.FloatField()

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Product
        fields = ['id', 'price', 'title', 'href', 'images']


class SaleProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели SaleProduct
    """
    product = ProductShortSerializer(read_only=True)
    dateFrom = serializers.DateTimeField(read_only=True, format="%H:%M %d-%m")
    dateTo = serializers.DateTimeField(read_only=True, format="%H:%M %d-%m")
    salePrice = serializers.FloatField()

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = SaleProduct
        fields = ['product', 'salePrice', 'dateFrom', 'dateTo']

    def to_representation(self, instance):
        """
        Переопределяет представление модели SaleProduct
        """
        a = super().to_representation(instance)
        return {**a.pop('product'), **a}


class AvatarSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Avatar
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Avatar
        fields = ['src', 'alt']


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Profile
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Profile
        fields = ['patronymic', 'phone']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор для изменения пароля
    """
    passwordCurrent = serializers.CharField(required=True)
    passwordNew = serializers.CharField(required=True)


class BasketProductsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели BasketProducts
    """
    product = ProductShortSerializer(read_only=True)

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = BasketProducts
        fields = ['product', 'count_in_basket']

    def to_representation(self, instance):
        """
        Переопределяет представление модели BasketProducts
        """
        a = super().to_representation(instance)
        return {**a.get('product'), 'count_in_basket': a.get('count_in_basket')}


class BasketSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Basket
    """
    id = serializers.IntegerField()
    products = BasketProductsSerializer(source='basketproducts_set.all', many=True, read_only=True)

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Basket
        fields = ['id', 'user', 'products']


class OrderProductsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели OrderProducts
    """
    product = ProductShortSerializer()

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = OrderProducts
        fields = ['id', 'order', 'product', 'count_in_order']

    def to_representation(self, instance):
        """
        Переопределяет представление модели OrderProducts
        """
        a = super().to_representation(instance)
        return {**a.get('product'), 'count_in_order': a.get('count_in_order')}

    def create(self, validated_data):
        """
        Выполняет создание нового объекта модели
        """
        return OrderProducts.objects.create(
            order_id=validated_data['order'].orderId,
            product_id=validated_data['product']['id'],
            count_in_order=validated_data['count_in_order'],
        )

    def update(self, instance, validated_data):
        """
        Выполняет обновление существующего объекта модели
        """
        instance.order = validated_data.get('order')
        instance.product_id = validated_data.get('product').get('id')
        instance.count_in_order = validated_data.get('count_in_order')
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order
    """
    products = OrderProductsSerializer(source='orderproducts_set.all', many=True, read_only=True)
    createdAt = serializers.DateTimeField(read_only=True, format="%H:%M %d-%m-%Y")
    totalCost = serializers.FloatField()
    deliveryCost = serializers.FloatField()

    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Order
        fields = ['user', 'orderId', 'createdAt', 'fullname', 'email', 'phone', 'deliveryType', 'paymentType',
                  'totalCost', 'deliveryCost', 'status', 'city', 'address', 'freeDelivery', 'products']

    def update(self, instance, validated_data):
        """
        Выполняет обновление существующего объекта модели
        """
        instance.fullname = validated_data.get('fullname')
        instance.email = validated_data.get('email')
        instance.phone = validated_data.get('phone')
        instance.deliveryType = validated_data.get('deliveryType')
        instance.paymentType = validated_data.get('paymentType')
        instance.status = validated_data.get('status')
        instance.totalCost = validated_data.get('totalCost')
        instance.deliveryCost = validated_data.get('deliveryCost')
        instance.city = validated_data.get('city')
        instance.address = validated_data.get('address')
        instance.freeDelivery = validated_data.get('freeDelivery')
        instance.products.set = validated_data.get('products')
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment
    """
    class Meta:
        """
        Метакласс для определения модели и полей модели, с которыми будет работать сериализатор
        """
        model = Payment
        fields = ['id', 'number', 'name', 'month', 'year', 'code', 'user', 'order', 'paid_for']
