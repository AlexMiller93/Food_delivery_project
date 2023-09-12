from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User

from accounts.models import Account
from accounts.permissions import ManagerOrReadOnly
from accounts.serializers import AccountSerializer


# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def all_users(request: Request):
#     """
#         List of all users, only for admin
#     """
#     users = User.objects.all()
#     serializer = UserSerializer(users, many=True)
#     return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_accounts(request: Request):
    """
        List of all accounts, only for admin
    """
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([ManagerOrReadOnly])
def workers(request: Request):
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
def get_account(request: Request, pk: int):
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


@api_view(["POST"])
@permission_classes([AllowAny])
def create_account(request: Request):
    """
        Create a new account with current user
    """
    serializer = AccountSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        account = Account.objects.create()

        if account:
            response = {
                "message": "Account created!!!",
                "account_data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def account_detail(request: Request):
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
        serializer = AccountSerializer(account, data=request.data, many=True, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)