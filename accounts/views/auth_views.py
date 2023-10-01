from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, SignUpSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        token = Token.objects.get(user=request.user)
        token.delete()
        response = {"message": "Logout successfully!"}

        return Response(data=response, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = ([])

    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)

    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            username = serializer.data.get("username")
            password = serializer.data.get("password")
            if user := authenticate(username=username, password=password):
                token, created = Token.objects.get_or_create(user=user)

                response = {
                    "message": "Login successfully!",
                    "token": token.key,
                    "username": username
                }

                return Response(data=response, status=status.HTTP_200_OK)
            else:
                return Response(data={"message": "Invalid username or password"},
                                status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.GenericAPIView):
    permission_classes = ([])
    serializer_class = SignUpSerializer

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "User Created Successfully", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
