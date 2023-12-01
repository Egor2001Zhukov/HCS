from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views
from api.apps import ApiConfig

app_name = ApiConfig.name

router = DefaultRouter()
router.register(r'services', views.ServiceAPIViewSet, basename='services')
router.register(r'accrual', views.AccrualAPIViewSet, basename='accruals')
router.register(r'personal_account', views.PersonalAccountAPIViewSet, basename='personal_accounts')
router.register(r'reading', views.ReadingAPIViewSet, basename='readings')
router.register(r'subscription', views.SubscriptionAPIViewSet, basename='subscriptions')

urlpatterns = [path('health', views.health),
               ] + router.urls
