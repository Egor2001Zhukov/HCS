from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api import models, serializers


class AccrualAPIViewSet(ModelViewSet):
    queryset = models.Accrual.objects.all()
    serializer_class = serializers.AccrualSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class ServiceAPIViewSet(ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class PersonalAccountAPIViewSet(ModelViewSet):
    queryset = models.PersonalAccount.objects.all()
    serializer_class = serializers.PersonalAccountSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class ReadingAPIViewSet(ModelViewSet):
    queryset = models.Reading.objects.all()
    serializer_class = serializers.ReadingSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionAPIViewSet(ModelViewSet):
    queryset = models.SubscriptionToServices.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = [IsAuthenticated]


def health(request):
    return JsonResponse({"status": "ok"})
