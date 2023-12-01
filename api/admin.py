from django.contrib import admin

from api import models


@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(models.PersonalAccount)
class PersonalAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'number',)


@admin.register(models.Accrual)
class AccrualAdmin(admin.ModelAdmin):
    list_display = ('id', 'accrual_date', 'subscription')


@admin.register(models.Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('id', 'reading_date', 'subscription')


@admin.register(models.SubscriptionToServices)
class SubscriptionToServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active',)
