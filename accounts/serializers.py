from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

from rest_framework import serializers, status
from rest_framework.validators import ValidationError

from .models import Card, Account


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    username = serializers.CharField(min_length=5, max_length=25)
    password = serializers.CharField(min_length=8, max_length=20, write_only=True)
    password1 = serializers.CharField(min_length=8, max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "password1"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()
        username_exists = User.objects.filter(username=attrs["username"]).exists()

        password = attrs.get('password')
        password1 = attrs.get('password1')

        if password != password1:
            raise ValidationError(detail="Passwords doesn't match")

        if email_exists:
            raise ValidationError(detail="Email has already been used")

        if username_exists:
            raise ValidationError(detail="Username has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password1")

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'password']


class CardSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = Card
        fields = ('id', 'number', 'cvv', 'deadline')

    def create(self, validated_data):
        return Card(**validated_data)


class AccountSerializer(serializers.ModelSerializer):
    """    """
    user = SignUpSerializer(required=False, many=False)
    card = CardSerializer(required=False, many=False)

    class Meta:
        model = Account
        fields = ['id', 'user', 'user_type', 'gender', 'address', 'points', 'card']

    def create(self, validated_data):
        # user_data = validated_data.pop('user')
        # user = User.objects.create(**user_data)
        account = Account.objects.create(**validated_data)
        return account


class UserLoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(label="Username", write_only=True)
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
                raise serializers.ValidationError(msg, status='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, status='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
