import string
from random import *

from rest_framework.exceptions import ValidationError

from faker import Faker
faker = Faker()

def check_card_number(number):
    """
        Validate credit card number.
        Return Boolean value
    """
    double = 0
    total = 0
    digits = str(number)
    for i in range(len(digits) - 1, -1, -1):
        for c in str((double + 1) * int(digits[i])):
            total += int(c)
        double = (double + 1) % 2
    return (total % 10) == 0


def validate_card_number(number):
    """
        Check if card number has valid number
    """
    if not check_card_number(number):
        raise ValidationError("Card number is not valid, please rewrite one more time")
    print("Card was checked, number is valid")
    return number


def generate_number(length):
    random_number = ''.join(choice(string.digits) for _ in range(length))
    number = str(random_number)
    return number


def generate_valid_card_number():
    while True:
        digits = ''.join(choice(string.digits) for _ in range(16))
        if check_card_number(digits):
            break
    number = str(digits)
    return number


def create_list_valid_card_number():
    card_numbers = []
    for _ in range(10):
        num = generate_valid_card_number()
        card_numbers.append(num)
    return card_numbers


