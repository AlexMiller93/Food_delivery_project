from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import MenuItem


class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    food_name = serializers.CharField(max_length=200, required=True)
    kitchen = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=200)
    # images = serializers.ImageField()
    rating = serializers.FloatField(default=5.0)
    price = serializers.IntegerField()
    weight = serializers.IntegerField()
    # volume = serializers.IntegerField()
    published = serializers.BooleanField(default=False)


    class Meta:
        model = MenuItem
        # fields = '__all__'
        fields = ['id', 'food_name', 'kitchen', 'category',
                  'description', 'images', 'rating', 'price', 'weight', 'volume']

    def create(self, validate_data):
        """ 
        Create and return a new MenuItem instance, given the validated data.
        """

        menu_item = MenuItem(
            food_name=validate_data["food_name"],
            kitchen=validate_data["kitchen"],
            category=validate_data["category"],
            description=validate_data["description"],
            rating=validate_data["rating"],
            price=validate_data["price"],
            weight=validate_data["weight"],
            created_at=datetime.now(),

        )
        menu_item.save()
        return menu_item

    def update(self, instance, validated_data):
        """ 
        Update and return an existing `MenuItem` instance, given the validated data.
        """

        instance.food_name = validated_data.get('food_name', instance.food_name)
        instance.kitchen = validated_data.get('kitchen', instance.kitchen)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.images = validated_data.get('images', instance.images)
        instance.price = validated_data.get('price', instance.price)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.volume = validated_data.get('volume', instance.volume)
        instance.published = validated_data.get('published', instance.published)
        # instance.date_edited = datetime.now(),
        instance.save()
        return instance


