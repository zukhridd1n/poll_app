from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Account, AccountProfile


@receiver(signal=post_save, sender=Account)
def create_account_profile(sender, instance, created, **kwargs):
    if created:
        AccountProfile.objects.create(account=instance)
