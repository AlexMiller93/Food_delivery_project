from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Card, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email']
            )
            user.set_password(validated_data['password'])
            user.save()
            Token.objects.create(user=user)
            return user


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'number', 'cvv', 'deadline',)

    def create(self, validated_data):
        card = Card(
            bank=validated_data['bank'],
            number=validated_data['number'],
            cvv=validated_data['cvv'],
            deadline=validated_data['deadline']
        )

        card.save()
        return card


class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    card = CardSerializer()

    class Meta:
        model = Account
        fields = ('id', 'user', 'user_type', 'gender', 'address', 'points', 'card')

    def create(self, validated_data):
        account = Account(
            user_type=validated_data['user_type'],
            gender=validated_data['gender'],
            address=validated_data['address'],
        )
        account.save()
        return account


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
