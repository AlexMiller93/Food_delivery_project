from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from accounts.models import Card
from accounts.serializers import CardSerializer


### Card views

def check_card_number(number):
    """
        Validate credit card number.
        Return Boolean value
    """
    double = 0
    total = 0
    digits = number
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_cards(request: Request):

    """
        Get all cards, only for admin.
    """

    if request.method == 'GET':
        try:
            cards = Card.objects.all()
        except Card.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def all_user_cards(request: Request):
    """
        Get all user cards, only for current user.
    """
    if request.method == 'GET':
        try:
            cards = Card.objects.filter(user=request.user)
        except Card.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        number = request.data['number']
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid() and validate_card_number(number):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def get_user_card(request: Request, pk: int):
    """
        Retrieve update or delete a card instance.
        For all user_types
    """
    # get all user cards

    # card = get_object_or_404(Card)

    try:
        card = Card.objects.filter(user=request.user).get(pk=pk)
    except Card.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Handles GET method
    if request.method == 'GET':
        serializer = CardSerializer(card, many=False)
        return Response(serializer.data)

    # Handles PUT method - update all fields
    elif request.method == 'PUT':
        number = request.data['number']
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid() and validate_card_number(number):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handles PATCH method - update some fields
    elif request.method == 'PATCH':
        serializer = CardSerializer(card, data=request.data, partial=True)
        if serializer.is_valid():
            number = request.data['number']
            if number:
                if validate_card_number(number):
                    pass
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handles DELETE method
    elif request.method == 'DELETE':
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)