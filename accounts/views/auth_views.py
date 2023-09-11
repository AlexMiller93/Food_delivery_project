from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from accounts.serializers import LoginSerializer, UserSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request: Request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request):
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
def user_login(request: Request):
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
def user_logout(request: Request):
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
def user_register(request: Request):
    if request.method == 'GET':
        return Response("Get method works")

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)