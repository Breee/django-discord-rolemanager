from django.core.management.base import BaseCommand
from donations.models import Donator, Donation, Transaction
from django.utils.timezone import now



class Command(BaseCommand):
    help = 'prepare users for new backend'

    def handle(self, *args, **kwargs):
        Donator.objects.all().update(balance=0.0,
                                     paid=0.0,
                                     fee=4.0,
                                     precious=False,
                                     monthly_paid=False,
                                     autopay=True,
                                     days_until_payment=0,
                                     updated=False,
                                     )
        Donation.objects.all().delete()
        Transaction.objects.all().delete()
