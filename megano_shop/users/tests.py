from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user
from django.urls import reverse

from users.models import Profile

TEST_PASSWORD = 'TestPassword'


class LoginAndRegistrationTest(TestCase):
    user = None

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='TestCase',
            password=TEST_PASSWORD,
        )
        cls.user = user
        Profile.objects.create(
            user=cls.user,
            phone='+79999999999',
            patronymic='string',
        )

    def test_users_registration_get_request(self):
        response = self.client.get(path=reverse('users:registration'))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='users/registration.html')

    def test_users_login_page_get_request(self):
        response = self.client.get(path=reverse('users:login'))
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='users/login_from.html')

    def test_users_registration_right_post_request(self):
        context = {
            'username': 'OrlovNickita',
            'first_name': 'Nikita',
            'last_name': 'Orlov',
            'patronymic': 'Yur',
            'phone': '+79999999999',
            'email': 'ttest@test.ru',
            'password1': TEST_PASSWORD,
            'password2': TEST_PASSWORD,
        }
        response = self.client.post(path=reverse('users:registration'),
                                    data=context, format='json')
        self.assertRedirects(response=response, expected_url=reverse('frontend:index'))
        self.assertTrue(User.objects.get(username='OrlovNickita'), True)

    def test_users_correct_login(self):
        self.assertFalse(get_user(self.client).is_authenticated)
        self.client.login(username=self.user.username,
                          password=TEST_PASSWORD)
        self.assertTrue(get_user(self.client).is_authenticated)
