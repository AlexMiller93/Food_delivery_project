from rest_framework import status, authentication, permissions, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.views import APIView

from ..models import Account
from ..permissions import ManagerOrReadOnly
from ..serializers import AccountSerializer


class AllAccountsView(generics.ListAPIView):
    """ """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AllWorkersView(generics.ListAPIView):
    """ """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = AccountSerializer

    def get_queryset(self):
        workers = Account.objects.filter('user_type' != 'Customer')
        return workers


class AccountAdminView(generics.RetrieveDestroyAPIView):
    """ """
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AccountCreateView(generics.CreateAPIView):
    """ """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

'''
@api_view(['GET'])
@permission_classes([])
def all_accounts(request: Request):
    """
        List of all accounts, only for admin
    """
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([ManagerOrReadOnly])
def all_workers(request: Request):
    """
        List of all accounts
        Only for manager
    """
    pass
    # user_type = request.data['user_type']
    # accounts = Account.objects.all()
    #
    # workers = Account.objects.filter(user_type == 'Customer')
    # serializer = AccountSerializer(workers, many=True)
    # return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([])
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
        serializer = AccountSerializer(account)
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
    if request.method == 'POST':
        data = {
            "user_type": request.data['user_type'],
            "points": request.data['points'],
            'gender': request.data['gender'],
            'address': request.data['address'],
        }
        serializer = AccountSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

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
'''


