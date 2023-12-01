from rest_framework import serializers

from api import models
from user.serializers import UserReadSerializer


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ['id', 'name', 'description', 'measure', 'price', 'consumption_standard']


class PersonalAccountSerializer(serializers.ModelSerializer):
    users = UserReadSerializer(read_only=True, many=True)

    class Meta:
        model = models.PersonalAccount
        fields = ['id', 'number', 'count_persons', 'square_meters', 'users']


class SubscriptionSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    personal_account = PersonalAccountSerializer()

    class Meta:
        model = models.SubscriptionToServices
        fields = ['id', 'shutdown_date', 'connect_date', 'is_active', 'service', 'personal_account', 'balance']


class AccrualSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = models.Accrual
        fields = ['id', 'summ', 'accrual_date', 'subscription', 'is_paid']


class ReadingSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()

    class Meta:
        model = models.Reading
        fields = ['id', 'value', 'reading_date', 'is_auto', 'subscription']
