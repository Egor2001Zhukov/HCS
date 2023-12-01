from django.db import models

from user.models import User


# Create your models here.


class Service(models.Model):
    MEASURE_CHOICES = [
        ('чел', 'за человека'),
        ('м2', 'за квадратный метр'),
        ('дн', 'за день'),
        ('м3', 'за кубический метр'),
        ('Гкал', 'за гигакалорию'), ]

    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    measure = models.CharField(max_length=150, verbose_name='Мера измерения', choices=MEASURE_CHOICES)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=11, decimal_places=2)
    consumption_standard = models.IntegerField(verbose_name='Нормативный расход', blank=True, null=True)
    is_necessary = models.BooleanField(verbose_name='Обязательная услуга')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class PersonalAccount(models.Model):
    number = models.IntegerField(verbose_name='Номер', unique=True)
    owner = models.CharField(max_length=150, verbose_name='Владелец')
    count_persons = models.IntegerField(verbose_name='Количество проживающих')
    square_meters = models.IntegerField(verbose_name='Количество квадратных метров')
    users = models.ManyToManyField(to=User, verbose_name='Пользователи',
                                   related_name='personal_account', blank=True)
    balance = models.DecimalField(verbose_name='Баланс', max_digits=11, decimal_places=2, default=0)
    auto_payment = models.BooleanField(verbose_name='Автоплатеж', default=False)

    def __str__(self):
        return f'PersonalAccount({self.number})'

    class Meta:
        verbose_name = 'Лицевой счет'
        verbose_name_plural = 'Лицевые счета'


class SubscriptionToServices(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='subscriptions', verbose_name='Услуга', null=True)
    personal_account = models.ForeignKey(PersonalAccount, on_delete=models.SET_NULL, related_name='subscriptions',
                                         verbose_name='Лицевой счет', null=True)
    shutdown_date = models.DateField(verbose_name='Дата отключения', blank=True, null=True)
    connect_date = models.DateField(verbose_name='Дата подключения', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активна', default=True)
    balance = models.DecimalField(verbose_name='Баланс', max_digits=11, decimal_places=2, default=0)


class Reading(models.Model):
    value = models.IntegerField(verbose_name='Значение')
    reading_date = models.DateField(verbose_name='Дата дачи показаний', auto_now_add=True)
    is_auto = models.BooleanField(verbose_name='Автоматически')
    subscription = models.ForeignKey(SubscriptionToServices, on_delete=models.SET_NULL, related_name='readings',
                                     verbose_name='Подключенная услуга', null=True)

    def __str__(self):
        return (f'Readings('
                f'Service({self.subscription.service.name})/'
                f'PersonalAccount({self.subscription.personal_account.number})/'
                f'Date({self.reading_date}))')

    class Meta:
        verbose_name = 'Показание'
        verbose_name_plural = 'Показания'


class Accrual(models.Model):
    accrual_date = models.DateField(verbose_name='Дата начисления', auto_now_add=True)
    is_paid = models.BooleanField(verbose_name='Оплачено', default=False)
    subscription = models.ForeignKey(SubscriptionToServices, on_delete=models.SET_NULL, related_name='accruals',
                                     verbose_name='Подключенная услуга', null=True)
    summ = models.DecimalField(verbose_name='Сумма к оплате', max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return (f'Accrual('
                f'Service({self.subscription.service.name})/'
                f'Date({self.accrual_date}))')

    class Meta:
        verbose_name = 'Начисление'
        verbose_name_plural = 'Начисления'
