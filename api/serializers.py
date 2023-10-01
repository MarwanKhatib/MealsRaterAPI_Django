from rest_framework import serializers
from .models import Meal, Rating
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "title", "description", "no_of_rating", "avg_rating"]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "stars", "user", "meal"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    # def create(self, validated_data):
    #     user = User.objects.create(**validated_data)
    #     return user
