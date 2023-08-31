from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import ManagerOrReadOnly
from .models import Account, Card
from .serializers import (AccountSerializer,
                          CardSerializer,
                          UserSerializer, LoginSerializer)


# Create your views here.


### Account views


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_users(request):
    """
        List of all users, only for admin
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_accounts(request):
    """
        List of all accounts, only for admin
    """
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([ManagerOrReadOnly])
def workers(request):
    """
        List of all accounts
        Only for manager
    """
    pass
    # user_type = request.data['user_type']
    # accounts = Account.objects.filter(user_type != 'Customer')
    # serializer = AccountSerializer(accounts, many=True)
    # return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAdminUser])
def get_account(request, pk):
    """
        Retrieve and delete an account profile
        Only for admin
    """
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account, many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def account_detail(request):
    """
        Retrieve update or delete an account instance.
        For all user_types
    """
    try:
        account = Account.objects.filter(user=request.user)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountSerializer(account, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


### Auth views


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

    """
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({
                "message": "You have logged in!!!",
                # "token": user.auth_token.key
            },
                status=status.HTTP_200_OK)
        return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
    """


@api_view(["POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        data = request.data

        username = data.get('username')
        password = data.get('password')
        user = None

        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'GET':
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    context = {}
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        account = Account.objects.get(user=user)

        context["username"] = user.get_username()
        context["token"] = token.key
        context["user_type"] = account.user_type
        return Response(context, status.HTTP_200_OK)
    else:
        context["errors"] = "You put wrong credentials"
        return Response(context, status.HTTP_401_UNAUTHORIZED)
'''


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def user_register(request):
    if request.method == 'GET':
        return Response("Get method works")

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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
def all_cards(request):
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
def all_user_cards(request):
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
def get_user_card(request, pk):
    """
        Retrieve update or delete a card instance.
        For all user_types
    """
    # get all user cards
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
