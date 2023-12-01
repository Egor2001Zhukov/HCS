from django.urls import path

from user.apps import UserConfig
from user import views

app_name = UserConfig.name
urlpatterns = [
    path('auth/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.UserCreateView.as_view(), name='register'),

]