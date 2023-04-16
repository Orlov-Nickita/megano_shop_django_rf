from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import RegistrationView, MyLoginView

app_name = 'users'

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', MyLoginView.as_view(), name='login'),
]
