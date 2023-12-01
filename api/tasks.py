from celery import shared_task

from api import models, services


@shared_task
def create_accruals():
    personal_accounts = models.PersonalAccount.objects.all()
    for personal_account in personal_accounts:
        new_accruals = []
        personal_subscriptions = personal_account.subscriptions.filter(is_active=True)
        for personal_subscription in personal_subscriptions:
            new_summ_accrual = services.calculation_accrual(personal_subscription)
            personal_subscription.balance += -new_summ_accrual
            personal_subscription.save()
            new_accrual = models.Accrual.objects.create(subscription=personal_subscription, summ=new_summ_accrual)
            new_accruals.append(new_accrual)
        services.send_payment_order(personal_account, new_accruals)
    return
