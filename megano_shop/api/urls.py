from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from api.views.ProfileAPIView import ProfileAPIView
from api.views.BannersAPIView import BannersAPIView
from api.views.BasketAPIView import BasketAPIView
from api.views.CatalogAPIView import CatalogAPIView
from api.views.CategoriesAPIView import CategoriesAPIView
from api.views.OrdersAPIView import OrdersAPIView
from api.views.OrderActiveAPIView import OrderActiveAPIView
from api.views.PaymentAPIVIew import PaymentAPIVIew
from api.views.PaymentProgressAPIView import PaymentProgressAPIView
from api.views.ProductAPIView import ProductAPIView
from api.views.ReviewAPIView import ReviewAPIView
from api.views.LimitedProductAPIView import LimitedProductAPIView
from api.views.PopularProductAPIView import PopularProductAPIView
from api.views.ProfileSetAvatarAPIView import ProfileSetAvatarAPIView
from api.views.ProfileSetPasswordAPIView import ProfileSetPasswordAPIView
from api.views.SalesAPIView import SalesAPIView
from api.views.TagAPIView import TagAPIView
from api.views.DeliveryCostAPIView import DeliveryCostAPIView

app_name = 'api'

schema_view = get_schema_view(
    openapi.Info(
        title='Megano SHOP API Specification',
        default_version='v1',
        description='Документация для работы с API магазина Megano SHOP',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='orlov.nickita@gmail.com'),
        license=openapi.License(name=''),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    path('account/', ProfileAPIView.as_view(), name='account'),
    path('banners/', BannersAPIView.as_view(), name='banners'),
    path('basket/', BasketAPIView.as_view(), name='basket'),
    path('catalog/', CatalogAPIView.as_view(), name='catalog'),
    path('catalog/<int:pk>/', CatalogAPIView.as_view(), name='catalog_num'),
    path('categories/', CategoriesAPIView.as_view(), name='categories'),
    path('orders/', OrdersAPIView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrdersAPIView.as_view(), name='orders_detail'),
    path('orders/active/', OrderActiveAPIView.as_view(), name='orders_active'),
    path('payment/', PaymentAPIVIew.as_view(), name='payment'),
    path('payment/progress/', PaymentProgressAPIView.as_view(), name='payment_progress'),
    path('product/<int:pk>/', ProductAPIView.as_view(), name='product_detail'),
    path('product/<int:pk>/review/', ReviewAPIView.as_view(), name='product_review'),
    path('products/limited/', LimitedProductAPIView.as_view(), name='product_limited'),
    path('products/popular/', PopularProductAPIView.as_view(), name='product_popular'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('profile/avatar/', ProfileSetAvatarAPIView.as_view(), name='profile_avatar'),
    path('profile/password/', ProfileSetPasswordAPIView.as_view(), name='profile_password'),
    path('sales/', SalesAPIView.as_view(), name='sales'),
    path('tags/', TagAPIView.as_view(), name='tags'),

    #### custom ####
    path('deliveryCost/<int:total_cost>/<str:delivery_type>', DeliveryCostAPIView.as_view(), name='deliveryCost'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
