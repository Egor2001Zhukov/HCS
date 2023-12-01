from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from user import models, serializers
from user.serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()
