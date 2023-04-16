from django import forms
from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib import messages
from django.utils.html import format_html
from frontend.models import Category, Tag, CategoryImage, Product, Review, ProductImage, Order, Basket, DeliveryCost, \
    SaleProduct, Specifications
from django.utils.translation import gettext_lazy as _


class SubcategoriesInline(admin.StackedInline):
    """
    Класс для отображения всех связанных с категориями соответствующих подкатегорий
    """
    model = Category.subcategory.through
    verbose_name = _('Категория')
    verbose_name_plural = _('Категории')
    fk_name = 'to_category'
    extra = 0

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'from_category':
            return db_field.remote_field.model.objects.filter(is_subcategory=False)
        return super(SubcategoriesInline, self).get_field_queryset(db, db_field, request)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Category (Категория)
    """
    inlines = [
        SubcategoriesInline
    ]
    list_display = ['id', 'title', 'href', 'photo_tag', 'is_subcategory', 'subcat_for']
    list_display_links = ['id', 'title']
    readonly_fields = ('href', 'photo_tag')
    fieldsets = (
        (None, {
            'fields': ('title', 'photo_tag',),
        }),
        (_('Дополнительная информация'), {
            'classes': ('wide',),
            'fields': ('image', 'is_subcategory'),
        }),
        (_('Подкатегории'), {
            'classes': ('collapse', 'wide'),
            'fields': ('subcategories',),
        }),
    )

    def photo_tag(self, obj):
        """
        Возвращает миниатюру изображения категории в общем списке, а также в карточке конкретной категории
        """
        if obj.image:
            return format_html(f'<img src="/media/{obj.image.src}" style="width:100px"')

    def subcat_for(self, obj):
        """
        Возвращает перечень категорий, для которых данный объект модели является подкатегорией
        """
        if obj.is_subcategory:
            center = ''
            for i in obj.subcategory.all():
                center += f'<a href="/admin/frontend/category/{i.id}/change/">{i}</a>'
            return format_html('<div>' + center + '</div>')
        return format_html('<span style="color:red">{}</span>'.format(_('Не является подкатегорией')))

    photo_tag.short_description = _('Миниатюра')
    subcat_for.short_description = _('Подкатегория для')

    def get_fieldsets(self, request, obj=None):
        """
        Если выбранный объект модели не является подкатегорией (а является категорией), то в данном случае
        отображаются все поля модели, в том числе и поле "подкатегории", в противном случае
        (когда объект - подкатегория) - поле "подкатегории" не отображается.
        """
        if obj and not obj.is_subcategory:
            return super(CategoryAdmin, self).get_fieldsets(request, obj)
        fields = tuple(
            item for item in self.fieldsets if item[0] != _('Подкатегории')
        )
        return fields

    def get_form(self, request, obj=None, **kwargs):
        """
        Если поле "подкатегории" не отображается, то под флагом "является подкатегорией" будет расположен
        вспомогательный текст (указан в атрибуте help_text модели), в противном случае вспомогательный текст
        будет не нужен - возвратиться пустая строка
        """
        form = super(CategoryAdmin, self).get_form(request, obj, **kwargs)
        if 'subcategories' in form.base_fields.keys():
            form.base_fields['is_subcategory'].help_text = ''
        return form

    def get_field_queryset(self, db, db_field, request):
        """
        Для поля модели "подкатегории" возвращает только те объекты модели, которые являются подкатегориями. Это
        необходимо для того, чтобы в списке отсутствовали категории, а были только подкатегории (объекты модели
        одинаковые, но благодаря атрибуту is_subcategory являются разноуровневыми, общие элементы и частные)
        """
        if db_field.name == 'subcategories':
            return db_field.remote_field.model.objects.filter(is_subcategory=True)
        return super(CategoryAdmin, self).get_field_queryset(db, db_field, request)


class ProductTagsInline(admin.StackedInline):
    """
    Класс для отображения всех связанных с тегами соответствующих продуктов
    """
    model = Tag.product_tags.through
    verbose_name = _('Товар')
    verbose_name_plural = _('Товары')
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Tag (Тег)
    """
    inlines = [
        ProductTagsInline,
    ]
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(CategoryImage)
class CategoryImageAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели CategoryImage (Изображение категории)
    """
    list_display = ['id', 'src', 'alt', 'photo_tag']
    list_display_links = ['id', 'alt']
    readonly_fields = ('photo_tag',)

    def photo_tag(self, obj):
        """
        Возвращает миниатюру изображения категории в общем списке, а также в карточке конкретной категории
        """
        if obj.src:
            return format_html(f'<img src="/media/{obj.src}" style="width:100px"')

    photo_tag.short_description = _('Миниатюра')


class SaleProductInline(admin.StackedInline):
    """
    Класс для отображения всех связанных с продуктом соответствующих распродаж
    """
    model = SaleProduct
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Product (Продукт)
    """
    inlines = [
        SaleProductInline
    ]
    list_display = ['id', 'title', 'price', 'count_in_stock', 'rating', 'category', 'available', 'freeDelivery',
                    'limited', 'banner', 'saled']
    list_display_links = ['id', 'title']
    list_editable = ['available', 'freeDelivery', 'limited', 'banner']
    fieldsets = (
        (_('Информация о товаре'), {
            'classes': ('wide',),
            'fields': ('title', 'description', 'fullDescription', 'category', 'rating'),
        }),
        (_('Количество и цена'), {
            'classes': ('collapse', 'wide'),
            'fields': ('price', 'count_in_stock', 'available', 'freeDelivery', 'limited'),
        }),
        (_('Реклама'), {
            'classes': ('collapse', 'wide'),
            'fields': ('banner',),
        }),
        (_('Дополнительная информация (Изображения, теги, отзывы и характеристики)'), {
            'classes': ('collapse', 'wide'),
            'fields': ('images', 'tags', 'reviews', 'specifications'),
        }),
    )

    def get_field_queryset(self, db, db_field, request):
        """
        Для поля "категории" отображаются только подкатегории
        Для поля "Характеристики" элементы отображаются отсортированными по имени и значению
        """
        if db_field.name == 'category':
            return db_field.remote_field.model.objects.filter(is_subcategory=True)
        if db_field.name == 'specifications':
            return db_field.remote_field.model.objects.order_by('name', '-value')
        return super(ProductAdmin, self).get_field_queryset(db, db_field, request)

    def saled(self, obj):
        """
        Возвращается количество продаж продукта
        """
        return Product.objects.filter(id=obj.id).aggregate(saled=Count('orderproducts__product')).get('saled')

    saled.short_description = _('Продано')


class MultiFileForm(forms.ModelForm):
    """
    Позволяет выполнять множественную загрузку фотографий для модели ProductImage (изображения продукта) за один раз
    """
    class Meta:
        model = ProductImage
        fields = 'file_field', 'alt'

    file_field = forms.ImageField(
        required=False,
        label=_('Фотографии'),
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        })
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели ProductImage (Изображения продукта)
    """
    list_display = ['id', 'file', 'alt', 'photo_tag']
    list_display_links = ['id', 'alt']
    readonly_fields = ('photo_tag',)
    # form = MultiFileForm

    def photo_tag(self, obj):
        """
        Возвращает миниатюру изображения категории в общем списке, а также в карточке конкретной категории
        """
        if obj.file:
            return format_html(f'<img src="/media/{obj.file}" style="width:100px"')

    # def save_model(self, request, obj, form, change):
    #     files = request.FILES.getlist('file_field')
    #     count = 1
    #     for f in files:
    #         obj.save()
    #         obj.file = f
    #         obj.alt = f'{form.cleaned_data.get("alt")} фото {count}'
    #         obj.save()
    #         count += 1
    #         obj.id += 1

    photo_tag.short_description = _('Миниатюра')


class ProductReviewInline(admin.StackedInline):
    """
    Класс для отображения всех связанных с продуктом соответствующих отзывов
    """
    model = Review.product_reviews.through
    verbose_name = _('Товар')
    verbose_name_plural = _('Товары')
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Review (Отзыв)
    """
    inlines = [
        ProductReviewInline
    ]
    list_display = ['id', 'author', 'email', 'text', 'rate']
    list_display_links = ['id', 'author']
    fieldsets = (
        (_('Отзыв'), {
            'classes': ('wide',),
            'fields': ('text', 'rate'),
        }),
        (_('Автор'), {
            'classes': ('collapse', 'wide'),
            'fields': ('author', 'email'),
        }),
    )


class OrderProductsInline(admin.StackedInline):
    """
    Класс для отображения всех связанных с заказом соответствующих продуктов
    """
    model = Order.products.through
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Order (Заказ)
    """
    list_display = ['orderId', 'fullname', 'phone', 'deliveryType', 'status', 'grand_total', 'city', 'createdAt']
    list_display_links = ['orderId', 'fullname']
    fieldsets = (
        (_('Информация о покупателе'), {
            'classes': ('collapse', 'wide'),
            'fields': ('user', 'fullname', 'email', 'phone'),
        }),
        (_('Информация о заказе'), {
            'classes': ('collapse', 'wide'),
            'fields': ('status', 'city', 'address')
        }),
        (_('Оплата и доставка'), {
            'classes': ('collapse', 'wide'),
            'fields': ('totalCost', 'deliveryCost', 'freeDelivery', 'deliveryType', 'paymentType')
        }),
    )
    inlines = [
        OrderProductsInline,
    ]

    def grand_total(self, obj: Order):
        """
        Возвращает общую сумму (общая стоимость товаров из заказа + стоимость доставки)
        """
        return obj.totalCost + obj.deliveryCost

    grand_total.short_description = _('Общая стоимость')
    grand_total.allow_tags = True


class ProductInline(admin.StackedInline):
    """
    Класс для отображения всех связанных с корзиной соответствующих продуктов
    """
    model = Basket.products.through
    extra = 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Basket (Корзина)
    """
    inlines = [
        ProductInline
    ]
    list_display = ['id', 'user']


@admin.register(DeliveryCost)
class DeliveryCostAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели DeliveryCost (Стоимость доставки)
    """
    list_display = ['title', 'money', 'description']

    def add_view(self, request, form_url='', extra_context=None):
        if self.model.objects.count() >= 3:
            self.message_user(
                request=request,
                message=_('Одновременно могут существовать только три записи - пожалуйста, сначала удалите другие'),
                level=messages.ERROR
            )
            return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_deliverycost_changelist'))
        return super().add_view(request, form_url, extra_context)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DeliveryCostAdmin, self).get_form(request, obj, **kwargs)
        for i in self.get_queryset(request):
            for j in form.base_fields.get('title').choices:
                if i.title == j[0]:
                    index = form.base_fields.get('title').choices.index(j)
                    del form.base_fields.get('title').choices[index]
        return form


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели SaleProduct (Распродажа)
    """
    list_display = ['id', 'product', 'salePrice', 'dateFrom', 'dateTo']


@admin.register(Specifications)
class SpecificationsAdmin(admin.ModelAdmin):
    """
    Класс для настроек и отображения в админ панели модели Specifications (Характеристики)
    """
    list_display = ['id', 'name', 'value']
