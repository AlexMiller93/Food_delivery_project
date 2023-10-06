import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from ..models import Card, Account
from ..utils import generate_valid_card_number
from ..serializers import AccountSerializer, CardSerializer

from faker import Faker

faker = Faker()


class AccountsTest(TestCase):
    """ Test module for GET all accounts API """

    def setUp(self) -> None:
        self.admin_user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=make_password(),
            is_staff=True
        )
        self.admin_card = Card.objects.create(
            bank='Test bank',
            number=generate_valid_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.admin_user
        )

        self.admin_account = Account.objects.create(
            user_type=random.choice(list(Account.USER_TYPES)),
            points=faker.pyint(min_value=0, max_value=500, step=10),
            gender=random.choice(list(Account.GENDERS)),
            address=faker.simple_profile()["address"],
            user=self.admin_user,
            card=self.admin_card
        )
        self.user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=make_password(),
        )
        self.card = Card.objects.create(
            bank='Test bank 2',
            number=generate_valid_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.user
        )

        self.account = Account.objects.create(
            user_type=random.choice(list(Account.USER_TYPES)),
            points=faker.pyint(min_value=0, max_value=500, step=10),
            gender=random.choice(list(Account.GENDERS)),
            address=faker.simple_profile()["address"],
            user=self.user,
            card=self.card
        )

    def test_get_all_accounts(self):
        client = APIClient()
        client.force_authenticate(self.admin_user)

        response = client.get(reverse('accounts:all_accounts'))
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_account(self):
        # TODO: add admin authentication

        client = APIClient()
        client.force_authenticate(self.admin_user)

        response = client.get(reverse(
            'accounts:get_account',
            kwargs={'pk': self.account.pk})
        )

        accounts = Account.objects.get(pk=self.account.pk)
        serializer = AccountSerializer(accounts)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_account(self):
        # TODO: add admin authentication

        client = APIClient()
        client.force_authenticate(self.admin_user)

        response = client.get(reverse(
            'accounts:get_account',
            kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_account(self):
        client = APIClient()
        client.force_authenticate(self.admin_user)

        response = client.delete(reverse(
            'accounts:get_account',
            kwargs={'pk': self.card.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_create_account(self):
    #     client = APIClient()
    #     client.force_authenticate(self.user)
    #     data = {
    #         "user_type": random.choice(list(Account.USER_TYPES)),
    #         "points": faker.pyint(min_value=0, max_value=500, step=10),
    #         "gender": random.choice(list(Account.GENDERS)),
    #         "address": faker.simple_profile()["address"],
    #     }
    #
    #     response = client.post(
    #         '/users/account/add/', data, format='json'
    #     )
    #
    #     print("\nCreate account")
    #     print(response)
    #     # print(response.json())
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data["message"], "Account created!!!")


class AccountTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=make_password(),
        )

        self.card = Card.objects.create(
            bank='Test bank',
            number=generate_valid_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """

        url = reverse('accounts:create_account')
        data = {
            # "user": self.user,
            "user_type": 'Courier',
            "points": faker.pyint(min_value=0, max_value=500, step=10),
            "gender": 'Male',
            "address": faker.simple_profile()["address"],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)

    """
    ## template from stackoverflow.com
    def test_login(self):
        '''
        This will test successfull login
        '''
        data = {
            "full_name" : "full name",
            'email' : "email@gmail.com",
            'password' : "password"
            }

        User.objects.create(
            full_name = data.get('full_name'),
            email = data.get('email'),
            password = make_password(data.get('password'))
            )
        
        response = self.client.get(self.url, data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    """
