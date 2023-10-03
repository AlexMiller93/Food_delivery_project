from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from faker import Faker

faker = Faker()

client = APIClient()


class RegisterUserTest(TestCase):
    """ Test module for POST register user API """

    def setUp(self) -> None:
        self.username = 'test_user'
        self.email = 'test_user@mail.com'
        self.password = 'qwerty##123'

        # valid input data
        self.valid_user_data = {
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'password1': self.password,
        }

        # empty username
        self.invalid_user_data = {
            'email': self.email,
            'username': '',
            'password': self.password,
            'password1': self.password,
        }

        self.passwords_not_equal = {
            'email': self.email,
            'username': self.username,
            'password': self.password,
            'password1': 'secret##',
        }

        """
        self.username_exists = {
            'email': 'test@mail.com',
            'username': 'test_user',
            'password': 'secret##',
            'password1': 'secret##',
        }
        """

    def test_valid_register_post(self):
        response = client.post(
            reverse('accounts:register'), data=self.valid_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User Created Successfully")

    def test_invalid_register_post(self):
        response = client.post(
            reverse('accounts:register'), data=self.invalid_user_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_equal_passwords(self):
        response = client.post(
            reverse('accounts:register'), data=self.passwords_not_equal
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTest(TestCase):
    def setUp(self) -> None:
        self.username = 'test_user'
        self.email = 'test_user@mail.com'
        self.password = 'qwerty##123'

    def test_invalid_login_post(self):
        response = client.post(
            reverse('accounts:login'), data={
                'username': 'test-user',
                'password': 'qwerty##123'
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid username or password")


class TestRegister(APITestCase):
    """
        This will handle register testcases
    """

    def setUp(self) -> None:
        self.url = reverse('accounts:register')

    def test_register_post(self):
        """
            This will test register post method
        """

        data = {
            "email": "test_user@mail.com",
            "username": "test-user",
            "password": "qwerty##123",
            "password1": "qwerty##123"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User Created Successfully")

    def test_no_username(self):
        """
            This will test register post method
        """

        data = {
            "email": "test_user@mail.com",
            "username": "",
            "password": "qwerty##123",
            "password1": "qwerty##123"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_equals_passwords(self):
        """
            This will test register post method
        """

        data = {
            "email": "test_user@mail.com",
            "username": "",
            "password": "qwerty##123",
            "password1": "qwerty##123!!!"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLogin(APITestCase):
    """
        This will handle login testcases
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="test_user@mail.com",
            username="test-user",
            password="qwerty##123"
        )
        self.url = reverse('accounts:login')

    def test_login_post(self):
        """
            This will test successfull login post
        """
        data = {
            "username": "test-user",
            "password": "qwerty##123"
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successfully!")
        self.assertTrue(response.data["token"])

    def test_login_post_invalid_data(self):
        """
            This will test invalid login post
        """
        data = {
            "username": "test__user",
            "password": "qwerty##123"
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Invalid username or password")
