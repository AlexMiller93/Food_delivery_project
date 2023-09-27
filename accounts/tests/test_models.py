from datetime import *

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import Card

from faker import Faker

faker = Faker()


class CardTest(TestCase):
    """ """

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

    def test_string_repr(self):
        user = User.objects.get(username=self.user.username)
        user2 = User.objects.get(username=self.user2.username)
        self.assertEqual(
            self.card.__str__(),
            f"{self.user.username} card's with number {self.card.number}"
        )
        self.assertEqual(
            self.card2.__str__(),
            f"{self.user2.username} card's with number {self.card2.number}"
        )

