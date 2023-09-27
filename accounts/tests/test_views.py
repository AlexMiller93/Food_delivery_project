import json
from datetime import *

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from ..models import Card
from ..serializers import CardSerializer

from faker import Faker

faker = Faker()


class GetAllCardsTest(TestCase):
    """ Test module for GET all cards API """

    # TODO: add admin authentication
    def setUp(self):
        # self.admin = User.objects.create(username="admin", password="tatoda72")
        self.user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=faker.pystr()
        )
        self.card = Card.objects.create(
            bank='Test bank',
            number=faker.credit_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.user
        )
        self.user2 = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=faker.pystr()
        )
        self.card2 = Card.objects.create(
            bank='Test bank',
            number=faker.credit_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.user2
        )

    def test_get_all_cards(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.get(reverse('accounts:all_cards'))
        cards = Card.objects.all()
        serializer = CardSerializer(cards, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetUserCardsTest(TestCase):
    """ Test module for GET all user cards API """

    def setUp(self):
        self.user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=faker.pystr()
        )
        self.card = Card.objects.create(
            bank='Test bank',
            number=faker.credit_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.user
        )

    def test_get_all_user_cards(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.get(reverse('accounts:all_user_cards'))
        cards = Card.objects.filter(user=self.user)
        serializer = CardSerializer(cards, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCardUpdateDeleteTest(TestCase):
    """ Test module for GET single card, update card, delete card API """

    # TODO:

    def setUp(self) -> None:
        self.user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=faker.pystr()
        )
        self.card = Card.objects.create(
            bank='Test bank',
            number=faker.credit_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.user
        )
        self.user2 = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=faker.pystr()
        )
        self.card2 = Card.objects.create(
            bank='Test bank',
            number=faker.credit_card_number(),
            deadline=timezone.now(),
            cvv=faker.credit_card_security_code(),
            user=self.user2
        )

        self.card_new_data = {
            'bank': 'Test bank 2',
            'number': faker.credit_card_number(),
            'deadline': str(timezone.now()),
            'cvv': faker.credit_card_security_code(),
        }

    def get_valid_single_card(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.get(reverse(
            'accounts:get_user_card',
            kwargs={'pk': self.card.pk}
        ))
        card = Card.objects.get(pk=self.card.pk)
        serializer = CardSerializer(card)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_invalid_single_card(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.get(reverse(
            'accounts:get_user_card',
            kwargs={'pk': 5}
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_card(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.put(reverse(
            'accounts:get_user_card', kwargs={'pk': self.card.pk}
            ), data=self.card_new_data)
        card = Card.objects.get(pk=self.card.pk)
        serializer = CardSerializer(card)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_card(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.patch(reverse(
            'accounts:get_user_card', kwargs={'pk': self.card.pk}
            ), data={'number': faker.credit_card_number()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_card(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.delete(reverse(
            'accounts:get_user_card', kwargs={'pk': self.card.pk}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CreateNewCardTest(TestCase):
    """ Test module for POST create card API """

    def setUp(self) -> None:
        self.user = User.objects.create(
            email=faker.simple_profile()["mail"],
            username=faker.simple_profile()["username"],
            password=faker.pystr()
        )

        self.valid_card_params = {
            'bank': 'Test bank',
            'number': faker.credit_card_number(),
            'deadline': str(timezone.now()),
            'cvv': faker.credit_card_security_code(),
        }

    def test_create_card(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.post(
            '/users/account/cards/', self.valid_card_params, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


