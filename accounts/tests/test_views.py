from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from ..serializers import *


### Useful links
# https://b0uh.github.io/djangodrf-how-to-authenticate-a-user-in-tests.html
# https://webdevblog.ru/razrabotka-na-osnove-testov-django-restful-api/
# https://github.com/encode/django-rest-framework/blob/master/tests/authentication/test_authentication.py

class AuthTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='test_user',
            password='qwerty##',
            email='test_user@example.com'
        )

    def test_force_authenticate(self):
        """test force_authenticate"""
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.assertTrue(self.token.key)

    def test_user_login(self):
        """test user login"""
        self.client.login(username=self.user.username, password=self.user.password)
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.assertTrue(self.token.key)


"""
class AuthTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('users/', include('accounts.urls')),
    ]

    def test_create_user(self):
        url = reverse('register')
        data = {
            "email": "test@example.com",
            "username": "test",
            "password": "qwerty##",
            "password1": "qwerty##",
        }

        response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "test")
"""


# class LoginViewTest(TestCase):
#     """ Test module for login views  """
#
#     # client.post('/notes/', {'title': 'new idea'}, format='json')
#     # client.login(username='lauren', password='secret')
#
#     def setUp(self, password=None):
#         self.user = get_user_model().objects.create_user(
#             username='test',
#             password='qwerty##',
#             email='test@example.com'
#         )
#         self.user.save()
#
#     def test_valid_params(self):
#         user = authenticate(username='test', password='qwerty##')
#         token, created = Token.objects.get_or_create(user=user)
#         # self.assertEqual(token.key, token.key)
#         self.assertTrue((user is not None) and user.is_authenticated)
#
#     def test_wrong_password(self):
#         user = authenticate(username='test', password='qwerty123')
#         self.assertFalse((user is not None) and user.is_authenticated)
#
#     def test_wrong_username(self):
#         user = authenticate(username='test__', password='qwerty123')
#         self.assertFalse((user is not None) and user.is_authenticated)
#
#     def test_get_valid_register(self):
#         pass
#         # response = self.client.get(reverse('register'))
#         #
#         # users = User.objects.all()
#         # serializer = SignUpSerializer(users)
#         # self.assertEqual(response.data, serializer.data)
#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_get_invalid_register(self):
#         pass
#
#     def test_login(self):
#         pass


class CardsViewTest(APITestCase):

    def setUp(self) -> None:
        pass

    def test_get_all_cards(self):
        pass

    def test_get_all_user_cards(self):
        pass

    def test_get_user_card(self):
        pass
