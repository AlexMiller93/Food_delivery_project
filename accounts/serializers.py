from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Card, Account


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],

        )
        user.save()

        account = Account(
            user=user,
            user_type=validated_data['user_type']
        )
        account.save()
        return account


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('number', 'cvv', 'deadline')

    def create(self, validated_data):
        card = Card(
            number=validated_data['number'],
            cvv=validated_data['cvv'],
            deadline=validated_data['deadline']
        )

        card.save()
        return card


