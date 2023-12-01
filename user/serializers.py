from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'password']


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name']
