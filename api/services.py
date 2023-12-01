import os
from decimal import Decimal

import openpyxl
from django.core.mail import send_mail
from django.db.models.functions import datetime
from django.http import HttpResponse

from api import models


def calculation_accrual_on_readings(subscription: models.SubscriptionToServices) -> Decimal:
    """Обработка показаний и возврат суммы начисления по показаниям"""
    subscription_readings = subscription.readings.all()
    last_auto_readings = subscription_readings.filter(is_auto=True).order_by('-reading_date').first()
    last_readings = subscription_readings.order_by('-reading_date').first()
    day_difference = (datetime.timezone.now() - last_readings.reading_date).days
    new_value_reading = last_readings.value + (subscription.service.consumption_standard * day_difference)
    new_auto_reading = models.Reading.objects.create(is_auto=True, subscription=subscription, value=new_value_reading)
    return (new_auto_reading.value - last_auto_readings) * subscription.service.price


def calculation_accrual(subscription: models.SubscriptionToServices) -> Decimal:
    """Расчет суммы для начисления"""
    if subscription.service.measure == 'чел':
        return subscription.service.price * subscription.personal_account.count_persons
    elif subscription.service.measure == 'м2':
        return subscription.service.price * subscription.personal_account.square_meters
    elif subscription.service.measure == 'дн':
        last_accrual = subscription.accruals.order_by('-accrual_date').first()
        if last_accrual:
            day_difference = (datetime.timezone.now() - last_accrual.accrual_date).days
        else:
            day_difference = (subscription.connect_date - last_accrual.accrual_date).days
        return day_difference * subscription.service.price
    else:
        return calculation_accrual_on_readings(subscription)


def create_payment_order(personal_account: models.PersonalAccount, accruals: list):
    """Создаем и возвращаем сводку по начислениям"""
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f'СЧЕТ НА ОПЛАТУ(Лицевой счет {personal_account.number})'
    sheet.append(["Услуга", "Размер платы", "Начислено с учетом перерасчета"])
    for accrual in accruals:
        sheet.append([accrual.subscription.service.name, accrual.subscription.service.price, accrual.summ])
    return workbook


def create_link_for_download_payment_order(personal_account: models.PersonalAccount, accruals: list):
    payment_order = create_payment_order(personal_account, accruals)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="hcs__payment_order({datetime.timezone.now()}).xlsx"'
    payment_order.save(response)
    return response


def send_payment_order(personal_account, accruals: list):
    link = create_link_for_download_payment_order(personal_account, accruals)
    subject = f'ЖКХ СЧЕТ НА ОПЛАТУ(Лицевой счет {personal_account.number})'
    message = f'Добрый день! У вас есть новое начисление для отплаты ЖКУ. Скачать квитанцию - {link}'
    recipient_list = [user.email for user in personal_account.users]
    send_mail(subject=subject, message=message,
              from_email=os.getenv('EMAIL_HOST_USER'),
              recipient_list=recipient_list)
