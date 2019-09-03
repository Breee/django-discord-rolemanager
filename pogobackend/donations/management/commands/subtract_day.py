from django.core.management.base import BaseCommand
from donations.models import Donator
from django.db.models import F


class Command(BaseCommand):
    help = 'subtract a day from each donator.'

    def handle(self, *args, **kwargs):
        Donator.objects.all().update(days_until_payment=F('days_until_payment')-1)
        Donator.objects.filter(days_until_payment__lte=0).update(monthly_paid=False)
